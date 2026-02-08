import os
from datetime import datetime
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
        "Коллеги, доброе утро! ☀️\n\n"
        "Желаю всем успешной и продуктивной рабочей недели. Большая просьба:\n\n"
        "1️⃣ Проверьте таблицу FTE и убедитесь, что все данные заполнены корректно.\n"
        "2️⃣ Заполните таблицу 'Задачи/Достижения' до 15:00 завтра (вторник).\n\n"
        "После выполнения просьба поставить реакцию ✅, чтобы я видел, что всё готово.\n\n"
        "Спасибо!"
    )
    bot.send_message(chat_id=CHAT_ID, text=text)
    print(f"Сообщение отправлено в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Планировщик ======
def schedule_bot():
    scheduler = BackgroundScheduler(timezone=MOSCOW_TZ)

    # Планируем каждый понедельник в 10:00 МСК
    scheduler.add_job(
        send_message,
        'cron',
        day_of_week='mon',
        hour=10,
        minute=0
    )

    scheduler.start()
    print("🤖 Бот запущен. Ждём понедельника 10:00 (МСК)...")

# ====== Главный запуск ======
if __name__ == "__main__":
    schedule_bot()
    # Flask слушает порт, который Render назначает через переменную PORT
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
