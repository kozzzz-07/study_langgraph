import operator
from typing import Annotated

from pydantic import BaseModel, Field

from langchain_core.messages import BaseMessage


class State(BaseModel):
    query: str
    messages: Annotated[list[BaseMessage], operator.add] = Field(default=[])
