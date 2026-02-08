from telegram import Bot
from telegram.ext import Updater
from datetime import datetime, timedelta
import pytz
import os

# Получаем токен и chat_id из переменных окружения (secrets)
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Московское время
MOSCOW_TZ = pytz.timezone("Europe/Moscow")

def send_message(context):
    context.bot.send_message(
        chat_id=CHAT_ID,
        text="✅ Тестовое сообщение прямо сейчас!"
    )
    print("Сообщение отправлено!")

def main():
    # Используем Updater версии 22.x
    updater = Updater(TOKEN)
    job_queue = updater.job_queue

    # Время запуска через 5 минут
    now = datetime.now(MOSCOW_TZ)
    run_time = now + timedelta(minutes=5)

    # Планируем однократное выполнение
    job_queue.run_once(
        send_message,
        when=(run_time - now).total_seconds()
    )

    updater.start_polling()
    print(f"🤖 Бот запущен. Сообщение придёт примерно в {run_time.strftime('%H:%M:%S')} (МСК)")
    updater.idle()

if __name__ == "__main__":
    main()
