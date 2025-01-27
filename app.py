import os
from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.integration.aiohttp import BotFrameworkHttpAdapter
from botbuilder.schema import Activity
from bot.dialogs import MainDialog
from bot.bot import TeamsBot
from bot.config import Config

app_id = Config.APP_ID
app_password = Config.APP_PASSWORD
adapter_settings = BotFrameworkAdapterSettings(app_id, app_password)
adapter = BotFrameworkHttpAdapter(adapter_settings)

bot = TeamsBot(MainDialog())

async def messages(req):
    # Process incoming messages
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    return web.Response(status=response.status)

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, port=3978)
