import queue
import json
import time
from typing import Any, Optional

event_queue = queue.Queue()


def send_event(event_type: str, data: Any, event_id: Optional[str] = None):
    """
    イベントをキューに送信します。
    :param event_type: イベントのタイプ (例: "message", "workflow_status")
    :param data: 送信するデータ (辞書や文字列など)
    :param event_id: オプションのイベントID
    """
    # データをJSON文字列に変換
    json_data = json.dumps(data, ensure_ascii=False)

    # SSEフォーマットに変換
    sse_message = ""
    if event_id:
        sse_message += f"id: {event_id}\n"
    sse_message += f"event: {event_type}\n"
    sse_message += f"data: {json_data}\n\n"

    event_queue.put(sse_message)


def event_stream():
    """
    イベントストリームを生成します。
    クライアントへの接続が切断された場合、ループを終了します。
    """
    last_heartbeat_time = time.time()
    HEARTBEAT_INTERVAL = 15  # 秒ごとにハートビートを送信

    while True:
        try:
            # キューからイベントを取得、タイムアウトを設定してハートビートを送信できるようにする
            message = event_queue.get(timeout=HEARTBEAT_INTERVAL)
            yield message
            last_heartbeat_time = (
                time.time()
            )  # イベント送信後もハートビート時間をリセット

        except queue.Empty:
            # タイムアウトした場合、ハートビートを送信
            if time.time() - last_heartbeat_time >= HEARTBEAT_INTERVAL:
                yield ": heartbeat\n\n"  # SSEコメントとして送信
                last_heartbeat_time = time.time()
            continue  # イベントがないので再度キューをチェック

        except GeneratorExit:
            # クライアントが接続を切断した場合
            print("Client disconnected from SSE stream.")
            break
        except Exception as e:
            # その他の予期せぬエラー
            print(f"Error in event_stream: {e}")
            # クライアントにエラーを通知する試み
            try:
                error_data = json.dumps({"type": "error", "message": str(e)})
                yield f"event: error\ndata: {error_data}\n\n"
            except Exception:
                pass  # yieldでエラーが出た場合は握りつぶす
            break
