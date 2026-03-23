import os
import asyncio
from datetime import datetime
import pytz
from flask import Flask
from telegram import Bot, ParseMode
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")           # Telegram Bot Token
CHAT_ID = int(os.getenv("CHAT_ID"))  # Telegram chat_id
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Flask для Render ======
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# ====== Проверка дублирования ======
sent_flags = {
    "msg1": False,
    "msg2": False,
    "msg3": False,
    "msg4": False
}

# ====== Функции отправки ======
async def send_msg1():
    if sent_flags["msg1"]:
        return
    bot = Bot(TOKEN)
    text = (
        "⏰ Напоминание перед завершением рабочего дня\n\n"
        "Не забудьте внести данные в таблицу FTE перед выключением компьютера:\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=4'>FTE</a>."
    )
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)
    sent_flags["msg1"] = True
    print(f"Msg1 отправлено {datetime.now(MOSCOW_TZ)}")

async def send_msg2():
    if sent_flags["msg2"]:
        return
    bot = Bot(TOKEN)
    # Отправка текста
    text = (
        "📌 Напоминание\n\n"
        "Пожалуйста, заполните таблицу с ключевыми событиями по своим блокам:\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d7r1jh6FrbhBfshoOG9qIPB0TEm7A4/APBIK5pedZ0IpJVIjt1XxQbUEAr8tH2Q-ALzAYEVVJAw#tid=2'>Задачи/Достижения</a> до 12:00."
    )
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)
    # Настоящий опрос
    await bot.send_poll(
        chat_id=CHAT_ID,
        question="Вы заполнили таблицу Задачи/Достижения?",
        options=["✅ Заполнил", "❌ Не было запусков"],
        is_anonymous=False
    )
    sent_flags["msg2"] = True
    print(f"Msg2 отправлено {datetime.now(MOSCOW_TZ)}")

async def send_msg3():
    if sent_flags["msg3"]:
        return
    bot = Bot(TOKEN)
    text = "Проверьте, пожалуйста, балансы кабинетов перед выходными."
    await bot.send_message(chat_id=CHAT_ID, text=text)
    sent_flags["msg3"] = True
    print(f"Msg3 отправлено {datetime.now(MOSCOW_TZ)}")

async def send_msg4():
    if sent_flags["msg4"]:
        return
    bot = Bot(TOKEN)
    text = (
        "📅 Начало месяца\n\n"
        "Необходимо внести данные FTE за прошлый месяц."
    )
    await bot.send_message(chat_id=CHAT_ID, text=text)
    sent_flags["msg4"] = True
    print(f"Msg4 отправлено {datetime.now(MOSCOW_TZ)}")

# ====== Планировщик ======
def schedule_bot():
    scheduler = BackgroundScheduler(timezone=MOSCOW_TZ)

    # Тест: все сообщения через DateTrigger прямо сейчас
    now = datetime.now(MOSCOW_TZ)
    scheduler.add_job(lambda: asyncio.run(send_msg1()), trigger=DateTrigger(run_date=now))
    scheduler.add_job(lambda: asyncio.run(send_msg2()), trigger=DateTrigger(run_date=now))
    scheduler.add_job(lambda: asyncio.run(send_msg3()), trigger=DateTrigger(run_date=now))
    scheduler.add_job(lambda: asyncio.run(send_msg4()), trigger=DateTrigger(run_date=now))

    scheduler.start()
    print("🤖 Тестовый запуск: все сообщения запланированы прямо сейчас.")

# ====== Главный запуск ======
if __name__ == "__main__":
    schedule_bot()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
