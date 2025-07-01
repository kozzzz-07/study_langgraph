from graph.state import State
from graph.workflow import compiled
from dotenv import load_dotenv

load_dotenv()

initial_state = State(query="生成AIについて教えてください")
result = compiled.invoke(initial_state)


print(result)

# 画像化
# https://langchain-ai.github.io/langgraph/how-tos/graph-api/#png
# output_path = "graph.png"
# compiled.get_graph().draw_mermaid_png(output_file_path=output_path)
