import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"

@app.get("/")
def home():
    return "Choice movies bot is running"

@app.post("/webhook")
def webhook():
    update = request.get_json(silent=True) or {}

    post = update.get("channel_post")

    if post and post.get("video"):
        chat = post.get("chat", {})
        username = chat.get("username")

        if username:
            link = f"https://t.me/{username}/{post['message_id']}"

            requests.post(
                f"{API}/sendMessage",
                json={
                    "chat_id": chat["id"],
                    "text": f"🔗 Video Link\n{link}"
                },
                timeout=10
            )

    return "ok", 200

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
