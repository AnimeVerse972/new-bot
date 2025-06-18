import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiohttp import web

from anime_posts import anime_posts

# .env faylni yuklash
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = f"/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get('PORT', 8000))

CHANNELS = [int(ch.strip()) for ch in os.getenv("CHANNELS", "").split(",")]

bot = Bot(token=API_TOKEN, parse_mode="MarkdownV2")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# UptimeRobot uchun route
async def on_check(request):
    return web.Response(text="Bot ishlayapti!")

app = web.Application()
app.router.add_get("/", on_check)

# Majburiy obuna tekshirish
async def check_sub_channels(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ("left", "kicked"):
                return False
        except:
            return False
    return True

# Boshlang'ich buyruq
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    is_member = await check_sub_channels(message.from_user.id)
    if not is_member:
        btn = types.InlineKeyboardMarkup()
        for ch in CHANNELS:
            invite_link = await bot.export_chat_invite_link(ch)
            btn.add(types.InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=invite_link))
        btn.add(types.InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_subs"))
        await message.answer("Botdan foydalanish uchun quyidagi kanal(lar)ga obuna bo‘ling:", reply_markup=btn)
    else:
        await message.answer("Kod yuboring (masalan: 001):")

# Callback orqali obuna qayta tekshirish
@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def callback_check_subs(callback_query: types.CallbackQuery):
    is_member = await check_sub_channels(callback_query.from_user.id)
    if is_member:
        await bot.answer_callback_query(callback_query.id, text="✅ Obuna tekshirildi.")
        await bot.send_message(callback_query.from_user.id, "Kod yuboring (masalan: 001):")
    else:
        await bot.answer_callback_query(callback_query.id, text="❗ Hali ham obuna emassiz.", show_alert=True)

# Kod yuborilganda postni ko‘rsatish
@dp.message_handler(lambda msg: msg.text.isdigit())
async def post_sender(message: types.Message):
    code = message.text.strip()
    post = anime_posts.get(code)
    if not post:
        await message.reply("❌ Bunday kod topilmadi.")
        return

    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=post["chat_id"],
        message_id=post["message_id"],
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("▶️ TOMOSHA QILISH", url="https://t.me/YourChannel")  # o‘zingizga moslang
        )
    )

# Webhook funksiyalar
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
