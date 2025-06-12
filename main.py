import os
import logging
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive

# Token va kanal sozlamalari
API_TOKEN = os.environ.get('BOT_TOKEN')
CHANNELS = ['@AniVerseClip', '@StudioNovaOfficial']
ADMINS = ['6486825926', '7575041003']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

keep_alive()

# JSON fayldan ma'lumotlarni yuklab olish
def load_anime_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

anime_data = load_anime_data()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    not_subscribed = []

    for channel in CHANNELS:
        try:
            chat_member = await bot.get_chat_member(channel, user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
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

    # Kanalga obunani tekshirish
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                await message.answer(f"⛔ Iltimos, {channel} kanaliga obuna bo‘ling va qaytadan urinib ko‘ring.")
                return
        except:
            await message.answer(f"⚠️ {channel} kanal tekshiruvida xatolik. Iltimos, keyinroq urinib ko‘ring.")
            return

    text = message.text.strip()

    # Reklama va homiylik
    if text in ["📢 Reklama", "💼 Homiylik"]:
        if text == "📢 Reklama":
            await message.answer("Reklama uchun @DiyorbekPTMA ga murojat qiling. Faqat reklama bo‘yicha!")
        elif text == "💼 Homiylik":
            await message.answer("Homiylik uchun karta: 8800904257677885")
        return

    # Kod orqali data.json dan qidirish
    code = text.upper()
    for anime in anime_data:
        if anime.get("code", "").upper() == code:
            title = anime.get("title", "Noma'lum")
            desc = anime.get("description", "Tavsifi yo'q")
            link = anime.get("link", "Havola yo'q")

            markup = InlineKeyboardMarkup().add(
                InlineKeyboardButton("📥 Yuklab olish", url=link)
            )

            await message.answer(f"*{title}*\n\n{desc}", reply_markup=markup)
            return

    await message.answer("❌ Bunday kod topilmadi. Iltimos, to‘g‘ri anime kodini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
