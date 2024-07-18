from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import requests
import json

from FT_api.core.config import get_setting
from FT_api.db.session import get_db
from FT_api.models.user import User, UserAnswers
from FT_api.schemas.nutrient_analyzer import FoodIntake

router = APIRouter()
settings = get_setting()


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            "X-NCP-CLOVASTUDIO-API-KEY": self._api_key,
            "X-NCP-APIGW-API-KEY": self._api_key_primary_val,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self._request_id,
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "text/event-stream",
        }
        results = []
        with requests.post(
            self._host + "/testapp/v1/chat-completions/HCX-003",
            headers=headers,
            json=completion_request,
            stream=True,
        ) as r:
            lines = iter(r.iter_lines())
            for line in lines:
                if line:
                    data = line.decode("utf-8")
                    # print(data)  # 디버그용 출력
                    if "event:result" in data:
                        next_line = next(lines).decode("utf-8")
                        if next_line.startswith("data:"):
                            data_content = next_line[len("data:") :].strip()
                            json_data = json.loads(data_content)
                            content_json = json.loads(json_data["message"]["content"])
                            results.append(content_json)
        # for result in results:
        #     print(json.dumps(result, indent=2, ensure_ascii=False))


def calculate_cpf(completion_executor, user_input):
    preset_text = [
        {
            "role": "system",
            "content": '당신은 식품영양사입니다.\n먹은 음식의 탄단지를 단계로 알려주며, 섭취한 수분과 활동량도 단계로 구분해줍니다. 계산 단계는 아래와 같습니다. \n1. 사용자 정보 가지고 기초대사량 계산\n2. 활동 수준 고려하여 TDEE 계산\n3. 체중 목표(감량 혹은 증대)에 따른 권장 섭취 칼로리 계산\n- 감량 : 15% 감산, 증대 : 15 % 증산\n4. 목표 섭취 비율 계산\n5. 레벨 분석\n아래 정보를 가지고 사용자의 탄단지와 수분 섭취 단계를 json 형식으로 알려주세요.\n\n다만 목표 체중에 따라 레벨 판단 기준이 달라질 수 있습니다. \r\n\r\n### 목표 체중에 따른 레벨 판단 기준 조정\r\n\r\n#### 1. 체중 감량 목표 (칼로리 제한)\r\n\r\n\r\n##### 탄수화물 섭취 기준 (체중 감량 목표)\r\n- **일반적인 권장 섭취 비율**: 하루 총 칼로리의 45-55%\r\n- **단계**\r\n  - Lv 1: < 40%\r\n  - Lv 2: 40-45%\r\n  - Lv 3: 45-55%\r\n  - Lv 4: 55-60%\r\n  - Lv 5: > 60%\r\n\r\n##### 단백질 섭취 기준 (체중 감량 목표)\r\n- **일반적인 권장 섭취 비율**: 하루 총 칼로리의 15-25%\r\n- **단계**\r\n  - Lv 1: < 15%\r\n  - Lv 2: 15-18%\r\n  - Lv 3: 18-25%\r\n  - Lv 4: 25-30%\r\n  - Lv 5: > 30%\r\n\r\n##### 지방 섭취 기준 (체중 감량 목표)\r\n- **일반적인 권장 섭취 비율**: 하루 총 칼로리의 20-25%\r\n- **단계**\r\n  - Lv 1: < 15%\r\n  - Lv 2: 15-20%\r\n  - Lv 3: 20-25%\r\n  - Lv 4: 25-30%\r\n  - Lv 5: > 30%\r\n\r\n#### 2. 체중 유지 목표 (균형 잡힌 섭취)\r\n체중을 유지하려는 경우, 일반적인 권장 섭취 비율을 따르는 것이 좋습니다.\r\n\r\n##### 탄수화물 섭취 기준 (체중 유지 목표)\r\n- **일반적인 권장 섭취 비율**: 하루 총 칼로리의 55-65%\r\n- **단계**\r\n  - Lv 1: < 50%\r\n  - Lv 2: 50-55%\r\n  - Lv 3: 55-65%\r\n  - Lv 4: 65-70%\r\n  - Lv 5: > 70%\r\n\r\n##### 단백질 섭취 기준 (체중 유지 목표)\r\n- **일반적인 권장 섭취 비율**: 하루 총 칼로리의 10-20%\r\n- **단계**\r\n  - Lv 1: < 7%\r\n  - Lv 2: 7-10%\r\n  - Lv 3: 10-20%\r\n  - Lv 4: 20-25%\r\n  - Lv 5: > 25%\r\n\r\n##### 지방 섭취 기준 (체중 유지 목표)\r\n- **일반적인 권장 섭취 비율**: 하루 총 칼로리의 20-30%\r\n- **단계**\r\n  - Lv 1: < 15%\r\n  - Lv 2: 15-20%\r\n  - Lv 3: 20-30%\r\n  - Lv 4: 30-35%\r\n  - Lv 5: > 35%\r\n\r\n#### 3. 체중 증량 목표 (칼로리 증가)\r\n체중을 증량하려는 경우, 탄수화물과 지방 섭취를 늘리고 단백질 섭취를 적절히 유지하는 것이 중요합니다.\r\n\r\n##### 탄수화물 섭취 기준 (체중 증량 목표)\r\n- **일반적인 권장 섭취 비율**: 하루 총 칼로리의 60-70%\r\n- **단계**\r\n  - Lv 1: < 55%\r\n  - Lv 2: 55-60%\r\n  - Lv 3: 60-70%\r\n  - Lv 4: 70-75%\r\n  - Lv 5: > 75%\r\n\r\n##### 단백질 섭취 기준 (체중 증량 목표)\r\n- **일반적인 권장 섭취 비율**: 하루 총 칼로리의 10-20%\r\n- **단계**\r\n  - Lv 1: < 10%\r\n  - Lv 2: 10-12%\r\n  - Lv 3: 12-20%\r\n  - Lv 4: 20-25%\r\n  - Lv 5: > 25%\r\n\r\n##### 지방 섭취 기준 (체중 증량 목표)\r\n- **일반적인 권장 섭취 비율**: 하루 총 칼로리의 25-35%\r\n- **단계**\r\n  - Lv 1: < 20%\r\n  - Lv 2: 20-25%\r\n  - Lv 3: 25-35%\r\n  - Lv 4: 35-40%\r\n  - Lv 5: > 40%\r\n\r\n### 예시 계산 (체중 감량 목표)\r\n\r\n만약 하루에 2000칼로리를 섭취한다고 가정할 때, 체중 감량 목표를 위한 영양소 섭취 비율을 적용하면:\r\n\r\n- **탄수화물**: 900-1100 kcal (225-275g)\r\n  - Lv 1: < 200g\r\n  - Lv 2: 200-225g\r\n  - Lv 3: 225-275g\r\n  - Lv 4: 275-300g\r\n  - Lv 5: > 300g\r\n\r\n- **단백질**: 300-500 kcal (75-125g)\r\n  - Lv 1: < 75g\r\n  - Lv 2: 75-90g\r\n  - Lv 3: 90-125g\r\n  - Lv 4: 125-150g\r\n  - Lv 5: > 150g\r\n\r\n- **지방**: 400-500 kcal (44-56g)\r\n  - Lv 1: < 33g\r\n  - Lv 2: 33-44g\r\n  - Lv 3: 44-56g\r\n  - Lv 4: 56-67g\r\n  - Lv 5: > 67g\r\n\r\n이와 같은 방식으로 목표 체중에 맞춘 영양소 섭취 비율을 설정하여 식단을 평가하고 조절할 수 있습니다.\n\n\n이제 당신이 주어야할 답변의 예시는 아래와 같습니다.\n\n사용자 기본 정보:\n목표: 체중 감량\n성별: 여성\n생년월일: 1970년 1월 1일\n혈액형: O형\n키: 165cm\n몸무게: 65kg\n목표 몸무게: 55kg\n건강검진: 최근 건강검진 결과 이상 없음\n흡연: 비흡연\n질병: 없음\n가족력: 고혈압\n복용중인 약: 없음\n스트레스 정도: 보통\n\n\n설문 제공 정보: \n섭취한 음식 정보: 아침은 계란후라이, 우유 한 잔, 점심은 김치찌개, 쌀밥 한 공기, 저녁은 샐러드, 닭가슴살\n수분 섭취량: 2L\n간식 정보: 오후에 초콜릿 한 조각\n일일 활동량: 걷기 30분, 요가 30분\n에너지 수준: 8\n\n일때의 당신의 답변:\n{\n  "bmr": "1322.2 kcal",\n  "tdee": "2049.41 kcal",\n  "caloric_intake_for_weight_goal": "1742.0 kcal",\n  "carbohydrate_calculation": "아침(13g), 점심(80g), 저녁(10g), 간식(5g)으로 총 108g을 섭취하였습니다.(432 kcal, 총 섭취 칼로리의 24.8%) Lv 1. 매우 부족한 탄수화물 섭취 상태입니다. (하루 권장 탄수화물 섭취량 45-55%)",\n  "protein_calculation": "아침(15g), 점심(20g), 저녁(33g), 간식(0.5g)으로 총 68.5g을 섭취하였습니다. (총 섭취 칼로리의 15.7%) Lv 3. 적절한 단백질 섭취 상태입니다. (하루 권장 단백질 섭취량 15-25%)",\n  "fat_calculation": "아침(13g), 점심(10.5g), 저녁(4.5g), 간식(3g)으로 총 31g을 섭취하였습니다. (총 섭취 칼로리의 16%) Lv 2. 부족한 지방 섭취 상태입니다. (하루 총 지방 섭취량 20-25%)",\n  "carbohydrate_level": 1,\n  "protein_level": 3,\n  "fat_level": 2,\n  "hydration_level": 3\n}\n\n\n이제 주어진 사용자의 정보와 건강일지를 가지고 요구한 답변을 주세요.',
        },
        {
            "role": "user",
            "content": "사용자 기본 정보: 목표: 체중 감량 성별: 여성 생년월일: 1970년 1월 1일 혈액형: O형 키: 165cm 몸무게: 65kg 목표 몸무게: 55kg 건강검진: 최근 건강검진 결과 이상 없음 흡연: 비흡연 질병: 없음 가족력: 고혈압 복용중인 약: 없음\n\n\n설문 조사 제공 정보:\n섭취한 음식 정보: 아침은 시리얼, 점심은 샌드위치, 저녁은 된장찌개, 쌀밥 한 공기\n수분 섭취량: 1.5L\n간식 정보: 없음\n일일 활동량: 헬스장에서 근력 운동 1시간, 유산소 운동 30분\n에너지 수준: 9\n\n",
        },
        {
            "role": "assistant",
            "content": '{\n  "bmr": "1316.9 kcal",\n  "tdee": "2023.64 kcal",\n  "caloric_intake_for_weight_goal": "1721.48 kcal",\n  "carbohydrate_calculation": "아침(27g), 점심(50g), 저녁(69g)으로 총 146g을 섭취하였습니다.(575.6 kcal, 총 섭취 칼로리의 33.5%) Lv 2. 부족한 탄수화물 섭취 상태입니다. (하루 권장 탄수화물 섭취량 45-55%)",\n  "protein_calculation": "아침(20g), 점심(25g), 저녁(25g)으로 총 70g을 섭취하였습니다. (총 섭취 칼로리의 17.14%) Lv 3. 적절한 단백질 섭취 상태입니다. (하루 권장 단백질 섭취량 15-25%)",\n  "fat_calculation": "아침(11g), 점심(22g), 저녁(19g)으로 총 52g을 섭취하였습니다. (총 섭취 칼로리의 26.32%) Lv 3. 적절한 지방 섭취 상태입니다. (하루 총 지방 섭취량 20-25%)",\n  "carbohydrate_level": 2,\n  "protein_level": 3,\n  "fat_level": 3,\n  "hydration_level": 2\n}',
        },
        {"role": "user", "content": user_input},
    ]

    request_data = {
        "messages": preset_text,
        "topP": 0.8,
        "topK": 0,
        "maxTokens": 424,
        "temperature": 0.5,
        "repeatPenalty": 5.0,
        "stopBefore": [],
        "includeAiFilters": True,
        "seed": 0,
    }

    response_text = completion_executor.execute(request_data)
    return response_text


completion_executor = CompletionExecutor(
    host="https://clovastudio.stream.ntruss.com",
    api_key="NTA0MjU2MWZlZTcxNDJiY+s0q8GHpKNVEoR18hPokgBKzh79TtDEFN4a+6i3GP3w",
    api_key_primary_val="FATytQBFXwkk3OeVpYIPJG8L4cx1tgUuEFhYWi0b",
    request_id="b7b0b19f-cdcf-4ca0-bccd-80d46abd6962",
)

# user_data = "사용자 기본 정보: \
#     목표: 체중 감량 \
#     성별: 여성 \
#     생년월일: 1960년 1월 1일 \
#     혈액형: O형 \
#     키: 163cm \
#     몸무게: 68kg \
#     목표 몸무게: 65kg \
#     건강검진: 최근 건강검진 결과 이상 없음 \
#     흡연: 비흡연 \
#     질병: 당뇨 \
#     가족력: 고혈압 \
#     복용중인 약: 없음 \
#     스트레스 정도: 보통 \
# "

# user_survey = "설문 조사 제공 정보: \
#     섭취한 음식 정보: 아침은 떡국, 점심은 마라탕, 저녁은 된장찌개, 쌀밥 한 공기 \
#     수분 섭취량: 1.5L \
#     간식 정보: 없음 \
#     일일 활동량: 헬스장에서 근력 운동 3시간, 유산소 운동 30분 \
#     에너지 수준: 9 \
# "

# result = calculate_cpf(completion_executor, user_data + user_survey)


@router.post("")
def get_nutrient_info(food_intake: FoodIntake, db: Session = Depends(get_db)):
    """
        {
      "breakfast": "떡국",
      "lunch": "마라탕",
      "dinner": "된장찌개, 쌀밥 한 공기",
      "snacks": [],
      "water_intake": 1.5,
      "activity": "헬스장에서 근력 운동 3시간, 유산소 운동 30분",
      "energy_level": 9
    }
    """
    user = db.query(User).filter_by(id=67).first()
    user_ans = db.query(UserAnswers).filter_by(user_id=user.id).all()

    def get_answer(question_id):
        return next(
            (ans.answer for ans in user_ans if ans.question_id == question_id),
            "정보 없음",
        )

    user_data = f"""사용자 기본 정보: 
        목표: {get_answer(1)}
        성별: {user.gender}
        생년월일: {user.birthday}
        혈액형: {user.blood_type}형
        키: {user.height}cm
        몸무게: {user.weight}kg
        목표 몸무게: {user.target_weight}kg
        흡연: {get_answer(3)}
        질병: {get_answer(4)}
        가족력: {get_answer(5)}
        복용중인 약: {get_answer(6)}
        스트레스 정도: {get_answer(10)}
    """

    user_survey = f"""설문 조사 제공 정보:
        섭취한 음식 정보: 아침은 {food_intake.breakfast}, 점심은 {food_intake.lunch}, 저녁은 {food_intake.dinner}
        수분 섭취량: {food_intake.water_intake}L
        간식 정보: {"없음" if not food_intake.snacks else ",".join(food_intake.snacks)}
        일일 활동량: {food_intake.activity}
        에너지 수준: {food_intake.energy_level} 
        """

    print(user_data)
    print()
    print(user_survey)
    res = calculate_cpf(completion_executor, user_data + user_survey)
    print(res)
    return res
