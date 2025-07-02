# ペルソナを表すデータモデル
from typing import List
from pydantic import BaseModel, Field


class Persona(BaseModel):
    name: str = Field(..., description="ペルソナの名前")
    background: str = Field(..., description="ペルソナの持つ背景")


class Personas(BaseModel):
    personas: List[Persona] = Field(
        default_factory=list, description="ペルソナのリスト"
    )
