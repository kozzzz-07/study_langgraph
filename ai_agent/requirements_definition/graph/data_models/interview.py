from pydantic import BaseModel, Field

from .persona import Persona


# インタビュー内容を表すモデル
class Interview(BaseModel):
    persona: Persona = (Field(..., description="インタビュー対象のペルソナ"),)
    question: str = Field(..., description="インタビューでの質問")
    answer: str = Field(..., description="インタビューでの回答")


class InterviewResult(BaseModel):
    interviews: list[Interview] = Field(
        default_factory=list, description="インタビューの結果リスト"
    )
