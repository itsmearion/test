from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_IDS, ADMIN_CHANNEL
from utils.database import get_all_products, get_all_payments, save_order

app = Client("little_nocturne", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_state = {}  # user_id: {"step": ..., "data": {...}}

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_state[user_id] = {"step": None, "data": {}}

    sent = await message.reply("Selamat datang di Little Nocturne...", quote=True)
    await asyncio.sleep(3)
    await sent.delete()

    join_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Silakan Join Channel", url="https://t.me/littlenocturne")],
        [InlineKeyboardButton("Sudah Join", callback_data="joined")]
    ])
    await message.reply("Silakan join channel terlebih dahulu:", reply_markup=join_button)

@app.on_callback_query(filters.regex("joined"))
async def after_joined(client, callback):
    user_id = callback.from_user.id
    products = get_all_products()
    keyboard = [
        [InlineKeyboardButton(p[2], callback_data=f"product_{p[0]}")] for p in products
    ]
    await callback.message.edit("Pilih produk yang ingin kamu beli:", reply_markup=InlineKeyboardMarkup(keyboard))
    user_state[user_id] = {"step": "choose_product", "data": {}}

@app.on_callback_query(filters.regex("^product_(\\d+)"))
async def choose_variant(client, callback):
    product_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    product = next((p for p in get_all_products() if p[0] == product_id), None)
    if not product:
        return await callback.answer("Produk tidak ditemukan")

    user_state[user_id]["step"] = "choose_payment"
    user_state[user_id]["data"]["product"] = product

    payments = get_all_payments()
    keyboard = [
        [InlineKeyboardButton(pay[1], callback_data=f"pay_{pay[0]}")] for pay in payments
    ]
    await callback.message.edit(f"Kamu memilih: {product[2]}\nDurasi: {product[4]}\n\nPilih metode pembayaran:",
                                 reply_markup=InlineKeyboardMarkup(keyboard))

@app.on_callback_query(filters.regex("^pay_(\\d+)"))
async def request_proof(client, callback):
    user_id = callback.from_user.id
    payment_id = int(callback.data.split("_")[1])
    payment = next((p for p in get_all_payments() if p[0] == payment_id), None)
    if not payment:
        return await callback.answer("Metode pembayaran tidak ditemukan")

    user_state[user_id]["step"] = "wait_proof"
    user_state[user_id]["data"]["payment"] = payment
    await callback.message.edit("Silakan kirim bukti pembayaran (screenshot):")

@app.on_message(filters.photo & filters.private)
async def handle_proof(client: Client, message: Message):
    user_id = message.from_user.id
    state = user_state.get(user_id)
    if not state or state["step"] != "wait_proof":
        return

    order_data = state["data"]
    order_data["user"] = f"@{message.from_user.username}" if message.from_user.username else message.from_user.mention()
    order_data["photo"] = message.photo.file_id
    order_data["status"] = "Menunggu konfirmasi"

    # Simpan order ke database (opsional)
    save_order(user_id, order_data)

    # Kirim ke channel admin
    caption = (
        f"**Order Masuk!**\n"
        f"User: {order_data['user']}\n"
        f"Produk: {order_data['product'][2]} ({order_data['product'][4]})\n"
        f"Pembayaran: {order_data['payment'][1]}\n"
        f"Status: {order_data['status']}"
    )
    await client.send_photo(ADMIN_CHANNEL, photo=order_data['photo'], caption=caption)

    await message.reply("Tunggu sampai admin otw ke RC kamu.")
    user_state.pop(user_id, None)

app.run()
