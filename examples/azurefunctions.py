import logging
import azure.functions as func
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi


async def main(req: func.HttpRequest) -> func.HttpResponse:
    # create api client
    line_api = AioLineBotApi(channel_access_token="<YOUR CHANNEL ACCESS TOKEN>")

    # get events from request
    parser = WebhookParser(channel_secret="<YOUR CHANNEL SECRET>")
    events = parser.parse(
        req.get_body().decode("utf-8"),
        req.headers.get("X-Line-Signature", ""))

    for ev in events:
        # reply echo
        await line_api.reply_message(
            ev.reply_token,
            TextMessage(text=f"You said: {ev.message.text}"))

    # 200 response
    return func.HttpResponse("ok")
