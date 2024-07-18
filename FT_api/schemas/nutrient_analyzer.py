from pydantic import BaseModel, Field
from typing import List

class FoodIntake(BaseModel):
    breakfast: str
    lunch: str
    dinner: str
    snacks: List[str] = Field(default_factory=list)
    water_intake: float = Field(..., description="수분 섭취량(L)")
    activity: str = Field(..., description="일일 활동량")
    energy_level: int = Field(..., ge=0, le=10, description="에너지 수준 (0-10)")