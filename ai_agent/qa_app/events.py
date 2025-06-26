import queue

# イベントを管理するキュー
event_queue = queue.Queue()


def _generale_stream_message(message: str):
    yield f"data: {message}\n\n"


# イベントを送信する関数
def send_event(message: str):
    stream_message = _generale_stream_message(message)
    event_queue.put(stream_message)


# イベントストリームを生成する関数
def event_stream():
    while True:
        message = event_queue.get()
        yield from message
