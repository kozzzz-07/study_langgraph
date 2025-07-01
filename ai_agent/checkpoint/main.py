from graph.dump import print_checkpoint_dump
from graph.state import State
from graph.workflow import compiled_graph, checkpointer

config = {"configurable": {"thread_id": "example-1"}}


def test1():
    user_query = State(query="私の好きなものはずんだ餅です。覚えておいてね。")
    first_response = compiled_graph.invoke(user_query, config)
    print(first_response)

    for checkpoint in checkpointer.list(config):
        print(checkpoint)

    print_checkpoint_dump(checkpointer, config)


def test2():
    user_query = State(query="私の好物は何か覚えてる？")
    second_response = compiled_graph.invoke(user_query, config)
    print(second_response)

    for checkpoint in checkpointer.list(config):
        print(checkpoint)

    print_checkpoint_dump(checkpointer, config)


def test3():
    config2 = {"configurable": {"thread_id": "example-2"}}
    user_query = State(query="私の好物は何？")
    other_thread_response = compiled_graph.invoke(user_query, config2)
    print(other_thread_response)


def main():
    test1()
    test2()
    test3()


if __name__ == "__main__":
    main()
