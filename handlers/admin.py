from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import ADMIN_IDS
from bot.database.db import cur, conn

def register_admin(app):
    @app.on_message(filters.command("admin") & filters.user(ADMIN_IDS))
    async def admin_panel(client, message: Message):
        await message.reply_text(
            "Pilih tindakan admin:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Tambah Produk", callback_data="add_product")],
                [InlineKeyboardButton("➕ Tambah Metode Pembayaran", callback_data="add_payment")]
            ])
        )

    @app.on_callback_query(filters.regex("add_product"))
    async def ask_product(client, callback_query):
        await callback_query.message.edit_text("Kirim format:

kategori | nama | deskripsi | durasi")

        @app.on_message(filters.text & filters.user(ADMIN_IDS))
        async def receive_product(client, message):
            try:
                category, name, description, duration = [x.strip() for x in message.text.split("|")]
                cur.execute("INSERT INTO products (category, name, description, duration) VALUES (?, ?, ?, ?)", (category, name, description, duration))
                conn.commit()
                await message.reply_text("Produk berhasil ditambahkan!")
            except Exception as e:
                await message.reply_text(f"Gagal menambahkan produk: {e}")

    @app.on_callback_query(filters.regex("add_payment"))
    async def ask_payment(client, callback_query):
        await callback_query.message.edit_text("Kirim nama metode pembayaran:")

        @app.on_message(filters.text & filters.user(ADMIN_IDS))
        async def receive_payment(client, message):
            try:
                method = message.text.strip()
                cur.execute("INSERT INTO payments (method) VALUES (?)", (method,))
                conn.commit()
                await message.reply_text("Metode pembayaran berhasil ditambahkan!")
            except Exception as e:
                await message.reply_text(f"Gagal menambahkan metode pembayaran: {e}")