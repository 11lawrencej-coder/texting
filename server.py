from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

CHAT_FILE = "messages.json"

if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump([], f)


def load_messages():
    with open(CHAT_FILE, "r") as f:
        return json.load(f)


def save_messages(messages):
    with open(CHAT_FILE, "w") as f:
        json.dump(messages[-100:], f)


@app.route("/")
def home():
    return render_template_string(open("index.html").read())


@app.route("/messages")
def messages():
    return jsonify(load_messages())


@app.route("/send", methods=["POST"])
def send():
    data = request.json

    msgs = load_messages()

    msgs.append({
        "name": data["name"],
        "message": data["message"]
    })

    save_messages(msgs)

    return {"success": True}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )