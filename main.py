import os
import logging
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive

# Start time for uptime calculation
start_time = time.time()

# .env orqali token olish
API_TOKEN = os.environ.get('BOT_TOKEN')
CHANNELS = ['@AniVerseClip','@StudioNovaOfficial']

ADMINS = ['6486825926','7575041003']  # Admin IDlar

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

keep_alive()

def add_user(user_id):
    with open("users.txt", "a+") as f:
        f.seek(0)
        users = set(f.read().splitlines())
        if str(user_id) not in users:
            f.write(f"{user_id}\n")

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    add_user(user_id)

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
            keyboard.add(InlineKeyboardButton(f"\ud83d\udd14 {ch}", url=f"https://t.me/{ch.strip('@')}"))
        await message.answer("\ud83d\udccb *Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:*", reply_markup=keyboard)
        return

    buttons = [[KeyboardButton("\ud83d\udce2 Reklama"), KeyboardButton("\ud83d\udcbc Homiylik")]]
    if str(user_id) in ADMINS:
        buttons.append([KeyboardButton("\ud83d\udcca Bot statistikasi")])

    reply_markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("✅ Assalomu alaykum!\nAnime kodini yuboring (masalan: 1, 2, 3, ...)", reply_markup=reply_markup)

@dp.message_handler()
async def handle_code(message: types.Message):
    user_id = message.from_user.id
    add_user(user_id)

    if message.text == "\ud83d\udcca Bot statistikasi" and str(user_id) in ADMINS:
        with open("users.txt") as f:
            user_count = len(set(f.read().splitlines()))

        uptime_seconds = int(time.time() - start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours} soat {minutes} daqiqa"

        await message.answer(
            f"\ud83d\udcca *Bot Statistikasi*\n"
            f"\n\ud83d\udc64 Foydalanuvchilar: *{user_count}*"
            f"\n\ud83d\udd16 Admin: `{user_id}`"
            f"\n\u23f1 Ish vaqti: *{uptime_str}*",
            parse_mode="Markdown"
        )
        return

    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                await message.answer(f"\u26d4 Iltimos, {channel} kanaliga obuna bo‘ling va qaytadan urinib ko‘ring.")
                return
        except:
            await message.answer(f"\u26a0\ufe0f {channel} kanal tekshiruvida xatolik. Iltimos, keyinroq urinib ko‘ring.")
            return

    anime_posts = {
        "1": "*Donishmandning qayta tug'ilishi*\n\nhttps://t.me/AniVerseClip/10",
        "2": "*Baholovchi*\n\nhttps://t.me/AniVerseClip/23",
        "3": "*O'ta ehtiyotkor o'lmas qahramon*\n\nhttps://t.me/AniVerseClip/35",
        "4": "*Arifureta*\n\nhttps://t.me/AniVerseClip/49",
        "5": "*Qalqon qahramoni*\n\nhttps://t.me/AniVerseClip/76",
        "6": "*Qalqon qahramoni 2-fasl*\n\nhttps://t.me/AniVerseClip/104",
        "7": "*Oxiridan keyingi boshlanish*\n\nhttps://t.me/AniVerseClip/121",
        "8": "*Daho Shifokorning soyadagi yangi hayoti*\n\nhttps://t.me/AniVerseClip/127",
        "9": "*Qahramon Bo'lish X*\n\nhttps://t.me/AniVerseClip/131",
        "10": "*Real dunyodan haqiqiyroq o'yin*\n\nhttps://t.me/AniVerseClip/135",
        "11": "*Omadsizning qayta tug'ilishi*\n\nhttps://t.me/AniVerseClip/148",
        "12": "*O'zga dunyoda yolg'iz hujum*\n\nhttps://t.me/AniVerseClip/200",
        "13": "*Yigit va qiz o'rtasida do'stlik bo'lishi mumkinmi*\n\nhttps://t.me/AniVerseClip/216",
        "14": "*Yengilmas Bahamut yilnomalari*\n\nhttps://t.me/AniVerseClip/222",
        "15": "*Shikastlanishni istamasdim, shuning uchun himoyamni kuchaytirdim*\n\nhttps://t.me/AniVerseClip/235",
        "16": "*Jodugarlar jangi*\n\nhttps://t.me/AniVerseClip/260",
        "17": "*Kumush qirolning qayta tug'ulishi*\n\nhttps://t.me/AniVerseClip/360",
        "18": "*Elf rafiqamni qanday sevishim mumkin*\n\nhttps://t.me/AniVerseClip/379",
        "19": "*O'lik odamlar: Mo'jizalar mamlakati*\n\nhttps://t.me/AniVerseClip/392",
        "20": "*Meni oyga olib ket*\n\nhttps://t.me/AniVerseClip/405",
        "21": "*Goblinlar Qotili*\n\nhttps://t.me/AniVerseClip/430",
        "22": "*Soyada ko'tarilish*\n\nhttps://t.me/AniVerseClip/309",
        "23": "*Men kuchsiz qobilyatim bilan eng zo'ri bo'ldim va hammani yo'q qilaman*\n\nhttps://t.me/AniVerseClip/343",
        "24": "*Zanjirli qul*\n\nhttps://t.me/AniVerseClip/501",
        "25": "*Donishmandning nabirasi*\n\nhttps://t.me/AniVerseClip/514",
        "26": "*Bu ajoyib dunyo*\n\nhttps://t.me/AniVerseClip/462",
        "27": "*Qora chaqiruvchi*\n\nhttps://t.me/AniVerseClip/527",
        "28": "*Mexanik qo'llar*\n\nhttps://t.me/AniVerseClip/542",
        "29": "*O'zga dunyoda darajamni ko'tarib, bu dunyoda ham tengsiz bo'ldim*\n\nhttps://t.me/AniVerseClip/555",
        "30": "*Kemono voqeasi*\n\nhttps://t.me/AniVerseClip/569",
        "31": "*O'lim kundaligi*\n\nhttps://t.me/AniVerseClip/586",
        "32": "*Abadiylik qo'riqchisi*\n\nhttps://t.me/AniVerseClip/624",
        "33": "*O'zga dunyoda oilali boʻldim*\n\nhttps://t.me/AniVerseClip/638",
        "34": "*Sehr Yaratuvchi: Boshqa dunyoda qanday qilib sehr yaratish mumkin*\n\nhttps://t.me/AniVerseClip/665",
        "35": "*Farmatseft monologi*\n\nhttps://t.me/AniVerseClip/696",
        "36": "*Va'da qilingan Neverland*\n\nhttps://t.me/AniVerseClip/744"
    }

    code = message.text.strip()

    if code in anime_posts:
        await message.answer(f"\ud83d\udd0d Topildi:\n\n{anime_posts[code]}")
    elif code in ["\ud83d\udce2 Reklama", "\ud83d\udcbc Homiylik"]:
        if code == "\ud83d\udce2 Reklama":
            await message.answer("Reklama uchun @DiyorbekPTMA ga murojat qiling. Faqat reklama bo‘yicha!")
        elif code == "\ud83d\udcbc Homiylik":
            await message.answer("Homiylik uchun karta 8800904257677885")
    else:
        await message.answer("\u274c Bunday kod topilmadi. Iltimos, to‘g‘ri anime kodini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
