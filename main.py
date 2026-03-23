import os
from datetime import datetime
import pytz
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")           # Telegram Bot Token (Environment Variable)
CHAT_ID = int(os.getenv("CHAT_ID"))  # Telegram chat_id (Environment Variable)
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Асинхронная функция отправки ======
async def send_test_messages():
    bot = Bot(TOKEN)

    # 1️⃣ Напоминание перед завершением рабочего дня
    text1 = (
        "⏰ Напоминание перед завершением рабочего дня\n\n"
        "Не забудьте внести данные в "
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=4'>"
        "таблицу FTE</a> перед выключением компьютера."
    )
    await bot.send_message(chat_id=CHAT_ID, text=text1, parse_mode="HTML")

    # 2️⃣ Напоминание во вторник + опрос
    text2 = (
        "📌 Напоминание\n\n"
        "Пожалуйста, заполните "
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d7r1jh6FrbhBfshoOG9qIPB0TEm7A4/APBIK5pedZ0IpJVIjt1XxQbUEAr8tH2Q-ALzAYEVVJAw#tid=2'>"
        "таблицу с ключевыми событиями</a> по своим блокам до 12:00.\n\n"
        "После заполнения отметьтесь в опросе ниже 👇"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Заполнил", callback_data="filled"),
         InlineKeyboardButton("❌ Не было запусков", callback_data="not_filled")]
    ])
    await bot.send_message(chat_id=CHAT_ID, text=text2, parse_mode="HTML", reply_markup=keyboard)

    # 3️⃣ Напоминание перед выходными
    text3 = "⚠️ Проверьте, пожалуйста, балансы кабинетов перед выходными."
    await bot.send_message(chat_id=CHAT_ID, text=text3)

    # 4️⃣ Начало месяца
    text4 = (
        "📅 Начало месяца\n\n"
        "Необходимо внести данные FTE в Битрикс за прошлый месяц."
    )
    await bot.send_message(chat_id=CHAT_ID, text=text4)

    print(f"Тестовые сообщения отправлены в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Запуск теста ======
if __name__ == "__main__":
    asyncio.run(send_test_messages())
