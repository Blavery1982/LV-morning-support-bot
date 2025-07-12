import logging
from flask import Flask
from telegram.ext import Updater, CommandHandler
import schedule
import time
import threading
import pytz
from datetime import datetime

# === НАСТРОЙКИ ===
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

# === НАСТРОЙКА ЛОГГИРОВАНИЯ ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === FLASK СЕРВЕР ДЛЯ ПРОВЕРКИ ЖИЗНИ ===
app = Flask(__name__)

@app.route("/")
def index():
    return "Бот работает 🐥"

# === СООБЩЕНИЕ, ОТПРАВЛЯЕМОЕ ПО УТРАМ ===
def send_morning_message(context=None):
    message = "Доброе утро! ☀️ Сегодня твой день. Поддержка рядом. ✨"
    if context:
        context.bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        updater.bot.send_message(chat_id=CHAT_ID, text=message)

# === РАСПИСАНИЕ ДЛЯ ЕЖЕДНЕВНОЙ ОТПРАВКИ ===
def schedule_checker():
    tz = pytz.timezone("Asia/Almaty")  # Заменить на нужный тебе часовой пояс
    while True:
        now = datetime.now(tz)
        if now.hour == 8 and now.minute == 30:
            send_morning_message()
            time.sleep(60)  # Ждём минуту, чтобы не отправлять дубли
        time.sleep(20)

# === ОСНОВНАЯ ЛОГИКА БОТА ===
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я готов к утренним напоминаниям ☀️")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# === ЗАПУСК ===
if __name__ == '__main__':
    threading.Thread(target=schedule_checker, daemon=True).start()
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()
    updater.start_polling()
    updater.idle()