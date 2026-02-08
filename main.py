from datetime import datetime, timedelta

# Московское время
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

def send_message(context):
    context.bot.send_message(chat_id=CHAT_ID, text="✅ Тестовое сообщение прямо сейчас!")
    print("Сообщение отправлено!")

def main():
    updater = Updater(TOKEN)  # убрали use_context=True для версии 22.x
    job_queue = updater.job_queue

    # Время запуска через 1 минуту
    now = datetime.now(MOSCOW_TZ)
    run_time = now + timedelta(minutes=1)

    job_queue.run_once(send_message, when=(run_time - now).total_seconds())

    updater.start_polling()
    print(f"🤖 Тест запущен. Сообщение придёт примерно в {run_time.strftime('%H:%M:%S')} (МСК)")
    updater.idle()

if __name__ == "__main__":
    main()
