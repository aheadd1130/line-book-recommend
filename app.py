# line-book-recommend

from flask import Flask, request, abort
import random
import requests
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

BOOKS = [
    {
        "image": "https://i.imgur.com/xxxxxx.jpg",
        "text": "📘《書名 A》\n適合想慢下來、整理情緒的時候閱讀。"
    },
    {
        "image": "https://i.imgur.com/yyyyyy.jpg",
        "text": "📕《書名 B》\n如果你最近有點迷惘，這本很溫柔。"
    },
    {
        "image": "https://i.imgur.com/zzzzzz.jpg",
        "text": "📗《書名 C》\n給正在努力生活的你。"
    }
]

@app.route("/callback", methods=["POST"])
def callback():
    body = request.json
    events = body.get("events", [])

    for event in events:
        if event["type"] == "message":
            msg = event["message"]
            if msg["type"] == "text":
                text = msg["text"]
                reply_token = event["replyToken"]

                if "推薦" in text:
                    book = random.choice(BOOKS)
                    reply(reply_token, book)

    return "OK"

def reply(reply_token, book):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }

    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": "📚 書單幫你準備中～稍等一下下 💭"
            },
            {
                "type": "image",
                "originalContentUrl": book["image"],
                "previewImageUrl": book["image"]
            },
            {
                "type": "text",
                "text": book["text"]
            }
        ]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        json=payload
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
