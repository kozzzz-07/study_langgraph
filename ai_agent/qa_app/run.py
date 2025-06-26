from graph.state import State
from graph.workflow import compiled
from dotenv import load_dotenv

load_dotenv()

initial_state = State(query="生成AIについて教えてください")
result = compiled.invoke(initial_state)


print(result)
