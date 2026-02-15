import os
from datetime import datetime
import pytz
from flask import Flask
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")           # Telegram Bot Token (Environment Variable)
CHAT_ID = int(os.getenv("CHAT_ID"))  # Telegram chat_id (Environment Variable)

MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Flask для Render ======
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# ====== Асинхронная функция отправки ======
async def send_message_async():
    bot = Bot(TOKEN)
    text = (
        "Коллеги, доброе утро! ☀️\n\n"
        "Желаю всем успешной и продуктивной рабочей недели. Большая просьба:\n\n"
        "1️⃣ Проверьте таблицу <a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=1'>FTE</a> и убедитесь, что все данные заполнены корректно.\n"
        "2️⃣ Заполните таблицу <a href='https://docs.sbermarketing.ru:7052/d/s/12d7r1jh6FrbhBfshoOG9qIPB0TEm7A4/APBIK5pedZ0IpJVIjt1XxQbUEAr8tH2Q-ALzAYEVVJAw#tid=2'>Задачи/Достижения</a> до 15:00 завтра (вторник).\n\n"
        "После выполнения просьба поставить реакцию ✅, чтобы я видел, что всё готово.\n\n"
        "Не откладывайте на потом, чтобы не приходилось вас постоянно дергать.\n\n"
        "Спасибо!"
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="HTML"
    )

    print(f"Сообщение отправлено в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Планировщик ======
def schedule_bot():
    scheduler = BackgroundScheduler(timezone=MOSCOW_TZ)

    # Каждый понедельник в 10:00 МСК
    scheduler.add_job(
        lambda: asyncio.run(send_message_async()),
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
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
