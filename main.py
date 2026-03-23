import os
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import pytz

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")           # Telegram Bot Token (Environment Variable)
CHAT_ID = int(os.getenv("CHAT_ID"))  # Telegram chat_id (Environment Variable)

MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Асинхронная функция отправки сообщений ======
async def send_all_messages():
    bot = Bot(TOKEN)

    # 1️⃣ Каждый рабочий день (FTE)
    text1 = (
        "⏰ Напоминание перед завершением рабочего дня\n\n"
        "Не забудьте внести данные в таблицу FTE перед выключением компьютера:\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=4'>FTE</a>."
    )
    await bot.send_message(chat_id=CHAT_ID, text=text1, parse_mode="HTML")

    # 2️⃣ Вторник — Задачи/Достижения с опросом
    text2 = (
        "📌 Напоминание\n\n"
        "Пожалуйста, заполните таблицу с ключевыми событиями по своим блокам:\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d7r1jh6FrbhBfshoOG9qIPB0TEm7A4/APBIK5pedZ0IpJVIjt1XxQbUEAr8tH2Q-ALzAYEVVJAw#tid=2'>Задачи/Достижения</a> до 12:00.\n\n"
        "После заполнения обязательно отметьтесь в опросе ниже 👇"
    )

    # Кнопки опроса
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Заполнил", callback_data="filled")],
        [InlineKeyboardButton("❌ Не было запусков", callback_data="none")]
    ])
    await bot.send_message(chat_id=CHAT_ID, text=text2, parse_mode="HTML", reply_markup=keyboard)

    # 3️⃣ Пятница — Балансы кабинетов
    text3 = "📊 Проверка балансов\n\nПроверьте, пожалуйста, балансы кабинетов перед выходными."
    await bot.send_message(chat_id=CHAT_ID, text=text3)

    # 4️⃣ Первый рабочий день месяца — FTE за прошлый месяц
    text4 = "📅 Начало месяца\n\nНеобходимо заполнить FTE в битриксе за прошлый месяц."
    await bot.send_message(chat_id=CHAT_ID, text=text4)

    print(f"Все тестовые сообщения отправлены в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Запуск проверки ======
if __name__ == "__main__":
    asyncio.run(send_all_messages())
