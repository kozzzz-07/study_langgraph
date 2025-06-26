from langgraph.graph import StateGraph, END

from graph.nodes.answering import answering_node
from graph.nodes.check import check_node
from graph.nodes.selection import selection_node
from graph.state import State

workflow = StateGraph(State)
workflow.add_node("selection", selection_node)
workflow.add_node("answering", answering_node)
workflow.add_node("check", check_node)

# selectionノードから処理を開始
workflow.set_entry_point("selection")
# selectionノードからansweringノードへ
workflow.add_edge("selection", "answering")
# answeringノードからcheckノードへ
workflow.add_edge("answering", "check")


# checkノードから次のノードへの遷移に条件付きエッジを定義
# state.current_judgeの値がTrueならENDノードへ、Falseならselectionノードへ
workflow.add_conditional_edges(
    "check", lambda state: state.current_judge, {True: END, False: "selection"}
)

compiled = workflow.compile()
