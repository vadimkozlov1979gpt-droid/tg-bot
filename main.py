import os
import asyncio
from datetime import datetime
import pytz
from flask import Flask
from telegram import Bot, Poll
from apscheduler.schedulers.background import BackgroundScheduler

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Flask для Render ======
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# ====== Асинхронная функция отправки текста ======
async def send_text(text):
    bot = Bot(TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML")
    print(f"Сообщение отправлено {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Асинхронная функция отправки опроса ======
async def send_poll():
    bot = Bot(TOKEN)
    await bot.send_poll(
        chat_id=CHAT_ID,
        question="Вы заполнили таблицу Задачи/Достижения?",
        options=["✅ Заполнил", "❌ Не было запусков"],
        is_anonymous=False,
        type=Poll.REGULAR
    )
    print(f"Опрос отправлен {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Планируемые функции ======
def daily_fte_reminder():
    text = (
        "⏰ Напоминание перед завершением рабочего дня\n\n"
        "Не забудьте внести данные в "
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=4'>"
        "таблицу FTE</a> перед выключением компьютера."
    )
    asyncio.run(send_text(text))

def tuesday_tasks_poll():
    text = (
       "📌 Напоминание\n\n"
        "Пожалуйста, заполните "
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d7r1jh6FrbhBfshoOG9qIPB0TEm7A4/APBIK5pedZ0IpJVIjt1XxQbUEAr8tH2Q-ALzAYEVVJAw#tid=2'>"
        "таблицу с ключевыми событиями</a> по своим блокам до 12:00.\n\n"
        "После заполнения отметьтесь в опросе ниже 👇"
    )
    asyncio.run(send_text(text))
    asyncio.run(send_poll())

def friday_balance_check():
    text = "⚠️ Проверьте, пожалуйста, балансы кабинетов перед выходными."
    asyncio.run(send_text(text))

def first_workday_month():
    today = datetime.now(MOSCOW_TZ)
    # Если сегодня не будний день — выходим
    if today.weekday() >= 5:
        return
    # Проверяем: был ли ранее в этом месяце рабочий день
    for day in range(1, today.day):
        check_date = today.replace(day=day)
        if check_date.weekday() < 5:
            return  # Уже был рабочий день → не первый
    # Если дошли сюда → первый рабочий день месяца
    text = "📅 Начало месяца\n\nНеобходимо внести данные FTE за прошлый месяц."
    asyncio.run(send_text(text))

# ====== Планировщик ======
def schedule_bot():
    scheduler = BackgroundScheduler(timezone=MOSCOW_TZ)

    # 1) Ежедневно (пн-пт) в 18:50
    scheduler.add_job(daily_fte_reminder, 'cron', day_of_week='mon', hour=14, minute=5)

    # 2) Вторник в 11:00
    scheduler.add_job(tuesday_tasks_poll, 'cron', day_of_week='mon', hour=14, minute=6)

    # 3) Пятница в 18:00
    scheduler.add_job(friday_balance_check, 'cron', day_of_week='mon', hour=14, minute=7)

    # 4) Первый рабочий день месяца в 12:00
    scheduler.add_job(first_workday_month, 'cron', day_of_week='mon', hour=14, minute=8)

    scheduler.start()
    print("🤖 Бот запущен. Планировщик активен.")

# ====== Главный запуск ======
if __name__ == "__main__":
    schedule_bot()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
