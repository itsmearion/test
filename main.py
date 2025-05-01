import asyncio
from pyrogram import Client
from bot.config import API_ID, API_HASH, BOT_TOKEN
from bot.handlers.start import register_start
from bot.handlers.admin import register_admin

app = Client("little_nocturne", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

register_start(app)
register_admin(app)

if __name__ == "__main__":
    app.run()