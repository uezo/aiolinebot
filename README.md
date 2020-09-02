# aiolinebot

AioLineBotApi provides asynchronous interface for LINE messaging API

# ✨ Features

- 100% coverage: All endpoints of line-bot-sdk supported!
- 100% compatible: Both async and sync methods for each endpoint provided!
- Up-to-date immediately: Update automatically when your line-bot-sdk is updated!

by dynamic class building: making async api client at the first time you import this package, from the source of line-bot-sdk installed in your environment.

# 🥳 Usage

Just create instance of AioLineBotApi instead of LineBotApi. That's all.

```python
# line_api = LineBotApi("<YOUR CHANNEL ACCESS TOKEN>")
line_api = AioLineBotApi("<YOUR CHANNEL ACCESS TOKEN>")
```

Now you are ready to use both async and sync methods for each endpoint.

```python
# async
loop = asyncio.get_event_loop()
loop.run_until_complete(
    line_api.reply_message_async("<REPLY TOKEN>", TextMessage("Hello!"))
)

# sync
line_api.reply_message("<REPLY TOKEN>", TextMessage("Hello!"))
```

Note that when you get binary content by stream, you should close the http response after finished.

```python
content = await line_api.get_message_content_async("<MESSAGE ID>")
async for b in content.iter_content(1024):
    do_something(b)
await content.response.close()
```

# 📦 Installation

```
$ pip install aiolinebot
```

# ⚙ Dependencies

- aiohttp
- line-bot-sdk


# Contribution

All kinds of contributions are welcomed🙇‍♀️🙇‍♀️🙇‍♀️

Especially we need tests. Because of async we can't use `responses` that is used in the tests for line-bot-sdk. So at first we have to find out the way of testing...

If you have any ideas about testing post issue please🙏🙏

# 🥘 Example

This is the echobot on Azure Functions.

```python
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
    events = parser.parse(req.get_body().decode("utf-8"), req.headers.get("X-Line-Signature", ""))

    for ev in events:
        # reply echo
        await line_api.reply_message(ev.reply_token, TextMessage(text=f"You said: {ev.message.text}"))

    # 200 response
    return func.HttpResponse("ok")
```
