from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import ADMIN_IDS

def register_start(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message: Message):
        await message.reply_text(
            "Selamat datang di Little Nocturne. Silakan pilih produk kamu.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Channel", url="https://t.me/iPacarhaechannn")]]
            )
        )