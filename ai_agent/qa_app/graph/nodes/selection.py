from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from events import send_event
from graph.consts.roles import ROLES
from graph.state import State
from chat_model import llm


def selection_node(state: State) -> dict[str, Any]:
    query = state.query
    role_options = "\n".join(
        [f"{k}. {v['name']}: {v['description']}" for k, v in ROLES.items()]
    )
    prompt = ChatPromptTemplate.from_template(
        """質問を分析し、最も適切な回答担当ロールを選択してください。

選択肢:
{role_options}

回答は選択肢の番号（1、2、または3）のみを返してください。

質問: {query}
""".strip()
    )
    # 選択肢の番号のみを返すことを期待したいため、max_tokensの値を1に変更
    chain = (
        prompt
        | llm.with_config(configurable=dict(max_output_tokens=1))
        | StrOutputParser()
    )
    role_number = chain.invoke({"role_options": role_options, "query": query})

    send_event("role_selection", role_number)

    selected_role = ROLES[role_number.strip()]["name"]
    return {"current_role": selected_role}
