from pydantic import BaseModel

class SurveysRespSchema(BaseModel):
    id: int
    title: str
    description: str