# LLMからの応答を追加するノード関数
from typing import Any
from graph.state import State
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv


load_dotenv()


def llm_response(state: State) -> dict[str, Any]:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite-preview-06-17", temperature=0.5
    )
    ai_message = llm.invoke(state.messages)
    return {"messages": [ai_message]}
