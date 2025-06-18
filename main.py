import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
from aiohttp import web

API_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST", "https://new-bot-2-cet5.onrender.com")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 8000))

CHANNELS = ['@AniVerseClip', '@StudioNovaOfficial']
ADMINS = ['6486825926', '7575041003']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    not_subscribed = []

    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                not_subscribed.append(channel)
        except:
            not_subscribed.append(channel)

    if not_subscribed:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for ch in not_subscribed:
            keyboard.add(InlineKeyboardButton(f"🔔 {ch}", url=f"https://t.me/{ch.strip('@')}"))
        await message.answer("📛 *Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:*", reply_markup=keyboard)
        return

    buttons = [[KeyboardButton("📢 Reklama"), KeyboardButton("💼 Homiylik")]]
    reply_markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("✅ Assalomu alaykum!\nAnime kodini yuboring (masalan: 1, 2, 3, ...)", reply_markup=reply_markup)

@dp.message_handler()
async def handle_code(message: types.Message):
    user_id = message.from_user.id

    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                await message.answer(f"⛔ Iltimos, {channel} kanaliga obuna bo‘ling va qaytadan urinib ko‘ring.")
                return
        except:
            await message.answer(f"⚠️ {channel} kanal tekshiruvida xatolik. Iltimos, keyinroq urinib ko‘ring.")
            return

    anime_posts = {
        "1": {"channel": "@AniVerseClip", "message_id": 10},
        "2": {"channel": "@AniVerseClip", "message_id": 23},
        "3": {"channel": "@AniVerseClip", "message_id": 35},
        "4": {"channel": "@AniVerseClip", "message_id": 49},
        "5": {"channel": "@AniVerseClip", "message_id": 76},
        "6": {"channel": "@AniVerseClip", "message_id": 104},
        "7": {"channel": "@AniVerseClip", "message_id": 851},
        "8": {"channel": "@AniVerseClip", "message_id": 127},
        "9": {"channel": "@AniVerseClip", "message_id": 131},
        "10": {"channel": "@AniVerseClip", "message_id": 135},
        "11": {"channel": "@AniVerseClip", "message_id": 148},
        "12": {"channel": "@AniVerseClip", "message_id": 200},
        "13": {"channel": "@AniVerseClip", "message_id": 216},
        "14": {"channel": "@AniVerseClip", "message_id": 222},
        "15": {"channel": "@AniVerseClip", "message_id": 235},
        "16": {"channel": "@AniVerseClip", "message_id": 260},
        "17": {"channel": "@AniVerseClip", "message_id": 360},
        "18": {"channel": "@AniVerseClip", "message_id": 379},
        "19": {"channel": "@AniVerseClip", "message_id": 392},
        "20": {"channel": "@AniVerseClip", "message_id": 405},
        "21": {"channel": "@AniVerseClip", "message_id": 430},
        "22": {"channel": "@AniVerseClip", "message_id": 309},
        "23": {"channel": "@AniVerseClip", "message_id": 343},
        "24": {"channel": "@AniVerseClip", "message_id": 501},
        "25": {"channel": "@AniVerseClip", "message_id": 514},
        "26": {"channel": "@AniVerseClip", "message_id": 462},
        "27": {"channel": "@AniVerseClip", "message_id": 527},
        "28": {"channel": "@AniVerseClip", "message_id": 542},
        "29": {"channel": "@AniVerseClip", "message_id": 555},
        "30": {"channel": "@AniVerseClip", "message_id": 569},
        "31": {"channel": "@AniVerseClip", "message_id": 586},
        "32": {"channel": "@AniVerseClip", "message_id": 624},
        "33": {"channel": "@AniVerseClip", "message_id": 638},
        "34": {"channel": "@AniVerseClip", "message_id": 665},
        "35": {"channel": "@AniVerseClip", "message_id": 696},
        "36": {"channel": "@AniVerseClip", "message_id": 744},
        "37": {"channel": "@AniVerseClip", "message_id": 776},
        "38": {"channel": "@AniVerseClip", "message_id": 789},
        "39": {"channel": "@AniVerseClip", "message_id": 802},
        "40": {"channel": "@AniVerseClip", "message_id": 815},
        "41": {"channel": "@AniVerseClip", "message_id": 835},
        "42": {"channel": "@AniVerseClip", "message_id": 864},
        "43": {"channel": "@AniVerseClip", "message_id": 918},
        "44": {"channel": "@AniVerseClip", "message_id": 931},
        "45": {"channel": "@AniVerseClip", "message_id": 946}
    }

    code = message.text.strip()

    if code in anime_posts:
        channel = anime_posts[code]["channel"]
        message_id = anime_posts[code]["message_id"]

        keyboard = InlineKeyboardMarkup()
        watch_button = InlineKeyboardButton("TOMOSHA QILISH", url=f"https://t.me/{channel.strip('@')}/{message_id}")
        keyboard.add(watch_button)

        await bot.copy_message(chat_id=user_id, from_chat_id=channel, message_id=message_id, reply_markup=keyboard)

    elif code in ["📢 Reklama", "💼 Homiylik"]:
        if code == "📢 Reklama":
            await message.answer("Reklama uchun @DiyorbekPTMA ga murojat qiling.")
        elif code == "💼 Homiylik":
            await message.answer("Homiylik uchun karta: 8800904257677885")
    else:
        await message.answer("❌ Bunday kod topilmadi. Iltimos, to‘g‘ri anime kodini yuboring.")

# UptimeRobot uchun 200 OK
async def on_check(request):
    return web.Response(text="✅ Bot ishlayapti!", status=200)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

app = web.Application()
app.router.add_get("/", on_check)
app.router.add_post(WEBHOOK_PATH, dp.process_updates)  # ✅ to‘g‘ri

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        web_app=app,
    )
