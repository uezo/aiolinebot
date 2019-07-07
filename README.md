# aiolinebot

AioLineBotApi provides asynchronous interface for LINE messaging API

## Installation

```
$ pip install aiolinebot
```

## Dependencies

- aiohttp==3.5.4
- line-bot-sdk==1.12.1

## Usage

`linebot.LineBotApi`の初期化方法および各メソッドと互換性があります。

```python
# APIインターフェイスのインスタンス化
api = AioLineBotApi(channel_access_token="<YOUR CHANNEL ACCESS TOKEN>")

# 返信
await api.reply_message(reply_token, messages)
```

Azure Functionsでのおうむ返しBOTの実装例は以下の通り。

```python
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
```

ファイルダウンロードなどバイナリデータを利用するAPI（`linebot.models.Content`がリターンのメソッド）については、イテレーションによるデータ取得処理をサポートしているため、HTTPコネクションを維持したままアプリケーションにレスポンスデータを渡します。`async with`などでコンテキスト管理することでコネクションを閉じるようにしてください。

```python
async with api.get_rich_menu_image("RICHMENU ID") as content:
    async for b in content.iter_content():
        do_something(b)
```
