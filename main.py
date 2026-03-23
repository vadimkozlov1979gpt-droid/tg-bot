import os
from datetime import datetime
import pytz
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# ====== Асинхронная функция отправки ======
async def send_message_async(text, keyboard=None):
    bot = Bot(TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    print(f"Сообщение отправлено в {datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S')} МСК")

# ====== Тестовая отправка всех сообщений сразу ======
async def test_send_all():
    # 1️⃣ Напоминание перед завершением дня
    text_1 = (
        "⏰ Напоминание перед завершением рабочего дня\n\n"
        "Не забудьте внести данные в таблицу FTE перед выключением компьютера:\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d8kPNA16Yx4ebjWyCkZjhauOHofu8a/rTvtuzYiRiCttTZnk6vh0bCnoH9C3ffn-iLxAd9RXJAw#tid=4'>FTE</a>"
    )
    await send_message_async(text_1)

    # 2️⃣ Напоминание вторника с опросом
    text_2 = (
        "📌 Напоминание\n\n"
        "Пожалуйста, заполните таблицу с ключевыми событиями по своим блокам:\n"
        "<a href='https://docs.sbermarketing.ru:7052/d/s/12d7r1jh6FrbhBfshoOG9qIPB0TEm7A4/APBIK5pedZ0IpJVIjt1XxQbUEAr8tH2Q-ALzAYEVVJAw#tid=2'>Задачи/Достижения</a> до 12:00."
    )
    keyboard_2 = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Заполнил", callback_data="filled"),
         InlineKeyboardButton("❌ Не было запусков", callback_data="not_needed")]
    ])
    await send_message_async(text_2, keyboard_2)

    # 3️⃣ Проверка балансов в пятницу
    text_3 = "⚠️ Проверьте, пожалуйста, балансы кабинетов перед выходными."
    await send_message_async(text_3)

    # 4️⃣ Первый рабочий день месяца
    text_4 = "📅 Начало месяца\n\nНеобходимо внести данные FTE за прошлый месяц."
    await send_message_async(text_4)

# ====== Запуск теста ======
if __name__ == "__main__":
    asyncio.run(test_send_all())
