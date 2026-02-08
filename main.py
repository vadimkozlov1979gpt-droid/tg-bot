import os
from datetime import datetime, timedelta
import pytz
from flask import Flask
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")           # Telegram Bot Token (Environment Variable)
CHAT_ID = int(os.getenv("CHAT_ID"))  # Telegram chat_id (Environment Variable)

# Московское время
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Flask для Render ======
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# ====== Функции бота ======
def send_message():
    bot = Bot(TOKEN)
    text = (
        "✅ Тестовое сообщение!\n\n"
        "Если вы видите это сообщение, значит бот работает корректно."
    )
    bot.send_message(chat_id=CHAT_ID, text=text)
    print(f"Сообщение отправлено в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Планировщик ======
def schedule_bot():
    scheduler = BackgroundScheduler(timezone=MOSCOW_TZ)

    # Планируем однократное выполнение через 3 минуты
    run_time = datetime.now(MOSCOW_TZ) + timedelta(minutes=3)
    scheduler.add_job(
        send_message,
        'date',
        run_date=run_time
    )

    scheduler.start()
    print(f"🤖 Тестовый бот запущен. Сообщение придёт примерно в {run_time.strftime('%H:%M:%S')} МСК...")

# ====== Главный запуск ======
if __name__ == "__main__":
    schedule_bot()
    # Flask слушает порт, который Render назначает через переменную PORT
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
