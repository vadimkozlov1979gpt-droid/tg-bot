import os
from datetime import datetime
import pytz
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")           # Telegram Bot Token (Environment Variable)
CHAT_ID = int(os.getenv("CHAT_ID"))  # Telegram chat_id (Environment Variable)

MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Функция отправки ======
async def send_text(text, keyboard=None):
    bot = Bot(TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    print(f"Сообщение отправлено в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Сообщения ======
async def test_messages():
    # 1) Перед завершением рабочего дня
    text1 = (
        "⏰ Напоминание перед завершением рабочего дня\n\n"
        "Не забудьте внести данные в таблицу FTE перед выключением компьютера:\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=4'>FTE</a>"
    )
    await send_text(text1)

    # 2) Вторник / таблица Задачи/Достижения + опрос
    text2 = (
        "📌 Напоминание\n\n"
        "Пожалуйста, заполните таблицу с ключевыми событиями по своим блокам:\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d7r1jh6FrbhBfshoOG9qIPB0TEm7A4/APBIK5pedZ0IpJVIjt1XxQbUEAr8tH2Q-ALzAYEVVJAw#tid=2'>Задачи/Достижения</a> до 12:00.\n\n"
        "После заполнения обязательно отметьтесь в опросе ниже 👇"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Заполнил", callback_data="filled")],
        [InlineKeyboardButton("❌ Не было запусков", callback_data="none")]
    ])
    await send_text(text2, keyboard=keyboard)

    # 3) Пятница / балансы
    text3 = (
        "📊 Напоминание\n\n"
        "Проверьте, пожалуйста, балансы кабинетов перед выходными."
    )
    await send_text(text3)

    # 4) Первый рабочий день месяца / FTE за прошлый месяц
    text4 = (
        "📅 Начало месяца\n\n"
        "Необходимо внести данные FTE в битриксе за прошлый месяц."
    )
    await send_text(text4)

# ====== Запуск теста ======
if __name__ == "__main__":
    asyncio.run(test_messages())
