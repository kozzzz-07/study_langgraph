import time
import re
from google.api_core.exceptions import ResourceExhausted
from langchain_core.runnables import Runnable
from typing import TypeVar

T = TypeVar("T")


def invoke_with_retry(
    chain: Runnable[dict, T],
    params: dict,
    max_retries: int = 3,
    default_delay: int = 60,
) -> T:
    """
    リソース枯渇エラー（ResourceExhausted）に対応した再試行ロジックでLangChainのrunnableを実行します。

    Args:
        chain: 実行するLangChainのrunnable。
        params: runnableに渡すパラメータ。
        max_retries: 最大再試行回数。
        default_delay: APIから待機時間が提案されなかった場合のデフォルトの待機時間（秒）。

    Returns:
        runnableの実行結果。

    Raises:
        Exception: 最大再試行回数に達した場合。
    """
    retries = 0
    while retries < max_retries:
        try:
            return chain.invoke(params)
        except ResourceExhausted as e:
            print("ResourceExhausted:", e)

            # エラーメッセージから推奨される待機時間を抽出

            retry_delay_match = re.search(r"retry_delay {\s*seconds: (\d+)\s*}", str(e))

            print("ResourceExhausted:", retry_delay_match)

            if retry_delay_match:
                delay = int(retry_delay_match.group(1)) + 60  # 60秒バッファを追加
            else:
                delay = default_delay * (2**retries)  # 指数関数的バックオフ

            print(
                f"レートリミットを超えました。{delay}秒待機して再試行します... (試行 {retries + 1}/{max_retries})"
            )
            time.sleep(delay)
            retries += 1
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            raise e
    raise Exception(f"最大再試行回数 ({max_retries}) に達しました。")
