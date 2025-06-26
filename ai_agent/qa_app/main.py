from flask import Flask, Response, jsonify, request
from dotenv import load_dotenv

from events import event_stream, send_event
from graph.workflow import run_workflow


load_dotenv()
app = Flask(__name__)


@app.route("/sse")
def sse():
    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/run", methods=["POST"])
def run():
    data = request.json
    message = data.get("message")
    if not message:
        return "No message provided", 400

    send_event("status", "処理を開始します")
    run_workflow(message)
    send_event("status", "処理を終了します")
    return jsonify({"status": "success", "message": "Workflow initiated."}), 200


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
