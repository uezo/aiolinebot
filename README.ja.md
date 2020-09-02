# aiolinebot

AioLineBotApi は LINE messaging API に非同期インターフェイスを提供します。

# ✨ 特長

- 100% カバー: line-bot-sdkの全エンドポイントの非同期メソッドをサポート！
- 100% compatible: 非同期とLineBotApiと完全互換の同期メソッドの両方を提供！
- Up-to-date immediately: line-bot-sdkの更新に合わせて自動で更新！

これらの特長は、aiolinebotパッケージを初めてimportしたタイミングでインストールされているline-bot-sdkのソースから非同期クライアントモジュール（LineBotApiを継承）を自動生成することによって実現しています。

# 🥳 使い方

LineBotApiのかわりにAioLineBotApiのインスタンスを生成すればOKです。

```python
# line_api = LineBotApi("<YOUR CHANNEL ACCESS TOKEN>")
line_api = AioLineBotApi("<YOUR CHANNEL ACCESS TOKEN>")
```

これで非同期とこれまで利用してきた同期の両方のインターフェイスを利用することができます。

```python
# async
loop = asyncio.get_event_loop()
loop.run_until_complete(
    line_api.reply_message_async("<REPLY TOKEN>", TextMessage("Hello!"))
)

# sync
line_api.reply_message("<REPLY TOKEN>", TextMessage("Hello!"))
```

バイナリコンテンツをストリーミングによりダウンロードするときは、事後に必ず`response`を閉じるようにしてください。line-bot-sdk==1.16.0時点では`get_message_content_async`のみが対象のようです。

```python
content = await line_api.get_message_content_async("<MESSAGE ID>")
async for b in content.iter_content(1024):
    do_something(b)
await content.response.close()
```

# 📦 インストール

```
$ pip install aiolinebot
```

# ⚙ 依存パッケージ

- aiohttp
- line-bot-sdk


# コントリビューション

どんな種類のコントリビューションも大歓迎です🙇‍♀️🙇‍♀️🙇‍♀️

特にテストを提供してくださるとありがたいです。line-bot-sdkではAPIクライアントのテストに`responses`を利用していますが、非同期に対応していないため利用できません。どうしたらよいものか困っています・・・😖

よい方法をご存知の方がいらっしゃいましたら、どんなことでも結構ですのでIssueに投稿いただけると大変ありがたいです🙏🙏

# 🥘 実装例

Azure Functionsでのおうむ返しBOTの例です。

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
