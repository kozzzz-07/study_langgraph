LangGraphで作るAIエージェント実践入門の9章を参考に作成したアプリ

## セットアップ
- apikey
  - https://console.cloud.google.com/apis/credentials
  - set your GOOGLE_API_KEY

## 動作確認
- `cd ai_agent/qa_app`
- `uv run run.py`

## sse
- `uv run main.py`
- `curl http://127.0.0.1:5000/sse`
- `curl -X POST -H "Content-Type: application/json" -d '{"message": "生成AIに ついて教えて"}' http://127.0.0.1:5000/run`