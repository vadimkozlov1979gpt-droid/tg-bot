import os
import asyncio
from datetime import datetime
import pytz
from telegram import Bot

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")           # Telegram Bot Token
CHAT_ID = int(os.getenv("CHAT_ID"))  # Telegram chat_id

MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Функции отправки сообщений ======
async def send_message(text, parse_mode="HTML"):
    bot = Bot(TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=parse_mode)
    print(f"Сообщение отправлено в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

async def send_poll_message():
    bot = Bot(TOKEN)
    text = (
        "📌 Напоминание\n\n"
        "Пожалуйста, заполните таблицу с ключевыми событиями по своим блокам до 12:00:\n\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d7r1jh6FrbhBfshoOG9qIPB0TEm7A4/APBIK5pedZ0IpJVIjt1XxQbUEAr8tH2Q-ALzAYEVVJAw#tid=2'>Задачи/Достижения</a>\n\n"
        "После заполнения отметьтесь в опросе ниже 👇"
    )
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML")

    # Настоящий опрос
    question = "Вы заполнили таблицу?"
    options = ["✅ Заполнил", "❌ Не было запусков"]
    await bot.send_poll(chat_id=CHAT_ID, question=question, options=options, is_anonymous=False)
    print(f"Опрос отправлен в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Отправка всех сообщений сразу ======
async def send_all_now():
    # 1) Ежедневное сообщение
    await send_message(
        "⏰ Напоминание перед завершением рабочего дня\n\n"
        "Не забудьте внести данные в таблицу FTE перед выключением компьютера:\n\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=4'>FTE</a>"
    )

    # 2) Вторник – сообщение с опросом
    await send_poll_message()

    # 3) Пятница – проверка балансов
    await send_message(
        "🔔 Напоминание\n\nПроверьте, пожалуйста, балансы кабинетов перед выходными."
    )

    # 4) Первый рабочий день месяца – FTE за прошлый месяц
    await send_message(
        "📅 Начало месяца\n\n"
        "Необходимо заполнить FTE в битриксе за прошлый месяц:\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=4'>FTE</a>"
    )

# ====== Запуск ======
if __name__ == "__main__":
    asyncio.run(send_all_now())
