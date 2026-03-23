import os
import asyncio
from datetime import datetime
import pytz
from telegram import Bot

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")           # Telegram Bot Token (Environment Variable)
CHAT_ID = int(os.getenv("CHAT_ID"))  # Telegram chat_id (Environment Variable)
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Асинхронные функции ======
async def send_text(text):
    bot = Bot(TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML")
    print(f"Сообщение отправлено в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

async def send_poll():
    bot = Bot(TOKEN)
    await bot.send_poll(
        chat_id=CHAT_ID,
        question="Вы заполнили таблицу Задачи/Достижения?",
        options=["✅ Заполнил", "❌ Не было запусков"],
        is_anonymous=False
    )
    print(f"Опрос отправлен в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Сообщения ======
async def test_all_messages():
    # 1) Конец рабочего дня
    text1 = (
        "⏰ Напоминание перед завершением рабочего дня\n\n"
        "Не забудьте внести данные в таблицу FTE перед выключением компьютера: "
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=4'>FTE</a>."
    )
    await send_text(text1)

    # 2) Вторник — сообщение + опрос
    text2 = (
        "📌 Напоминание\n\n"
        "Пожалуйста, заполните таблицу с ключевыми событиями по своим блокам до 12:00: "
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d7r1jh6FrbhBfshoOG9qIPB0TEm7A4/APBIK5pedZ0IpJVIjt1XxQbUEAr8tH2Q-ALzAYEVVJAw#tid=2'>Задачи/Достижения</a>.\n\n"
        "После заполнения обязательно отметьтесь в опросе ниже 👇"
    )
    await send_text(text2)
    await send_poll()

    # 3) Пятница
    text3 = "Проверьте, пожалуйста, балансы кабинетов перед выходными."
    await send_text(text3)

    # 4) Первый рабочий день месяца
    text4 = "📅 Начало месяца\n\nНеобходимо внести данные FTE за прошлый месяц."
    await send_text(text4)

# ====== Запуск теста ======
if __name__ == "__main__":
    asyncio.run(test_all_messages())
