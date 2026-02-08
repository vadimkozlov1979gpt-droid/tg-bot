import os
from datetime import datetime, timedelta
import pytz
from flask import Flask
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

MOSCOW_TZ = pytz.timezone('Europe/Moscow')

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# ====== Асинхронная функция отправки ======
async def send_message_async():
    bot = Bot(TOKEN)
    text = "✅ Тестовое сообщение! Если вы видите это, бот работает."
    await bot.send_message(chat_id=CHAT_ID, text=text)
    print(f"Сообщение отправлено в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Планировщик ======
def schedule_bot():
    scheduler = BackgroundScheduler(timezone=MOSCOW_TZ)
    run_time = datetime.now(MOSCOW_TZ) + timedelta(minutes=3)

    # APScheduler не понимает async напрямую → оборачиваем в asyncio.run
    scheduler.add_job(lambda: asyncio.run(send_message_async()), 'date', run_date=run_time)

    scheduler.start()
    print(f"🤖 Тестовый бот запущен. Сообщение придёт примерно в {run_time.strftime('%H:%M:%S')} МСК...")

# ====== Главный запуск ======
if __name__ == "__main__":
    schedule_bot()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
