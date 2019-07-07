import logging

import azure.functions as func

from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi


async def main(req: func.HttpRequest) -> func.HttpResponse:
    # APIインターフェイスの初期化
    # api = LineBotApi(channel_access_token="<YOUR CHANNEL ACCESS TOKEN>")      # <-- 同期APIを利用した場合
    api = AioLineBotApi(channel_access_token="<YOUR CHANNEL ACCESS TOKEN>")

    # リクエストからイベントを取得
    parser = WebhookParser(channel_secret="<YOUR CHANNEL SECRET>")
    events = parser.parse(req.get_body().decode("utf-8"), req.headers.get("X-Line-Signature", ""))

    for ev in events:
        # おうむ返し
        # api.reply_message(ev.reply_token, TextMessage(text=f"You said: {ev.message.text}"))      # <-- 同期APIを利用した場合
        await api.reply_message(ev.reply_token, TextMessage(text=f"You said: {ev.message.text}"))

    # HTTPのレスポンス
    return func.HttpResponse("ok")
