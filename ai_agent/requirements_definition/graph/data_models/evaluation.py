# 評価の結果を表すモデル
from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    reason: str = Field(..., description="判断の理由")
    is_sufficient: bool = Field(..., description="情報が十分かどうか")
