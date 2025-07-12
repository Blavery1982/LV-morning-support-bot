import logging
from flask import Flask
from telegram.ext import Updater, CommandHandler
import schedule
import time
import threading
import pytz
from datetime import datetime
import random

# === НАСТРОЙКИ ===
TOKEN = "7959403046:AAFZlktYVS_CcmY_3QR-1ThxIZQgEOOERY8"
CHAT_ID = 257264245

# === ВОЗМОЖНЫЕ УТРЕННИЕ СООБЩЕНИЯ ===
MESSAGES = [
    "Доброе утро! ☀️ Сегодня твой день. Поддержка рядом. ✨",
    "Ты не одна. Мир полон добрых людей, и ты — одна из них 💛",
    "Позволь себе почувствовать опору внутри и начать день с теплом",
    "Ты можешь быть мягкой и сильной одновременно. Сегодня — твой день 🌿",
    "Всё, что нужно, уже внутри тебя. Просто дыши и иди в день 🌞",
]

QUESTIONS = [
    "Что я хочу подарить миру сегодня?",
    "Какая одна вещь сделает мой день наполненным?",
    "Что я могу сделать для себя с любовью прямо сейчас?",
    "Что бы я сказала себе, если бы была своей лучшей подругой?",
    "Какой я хочу быть в этом дне — несмотря ни на что?",
]

# === НАСТРОЙКА ЛОГГИРОВАНИЯ ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === FLASK СЕРВЕР ДЛЯ ПРОВЕРКИ ЖИЗНИ ===
app = Flask(__name__)

@app.route("/")
def index():
    return "Бот работает 🐥"

# === УТРЕННЕЕ СООБЩЕНИЕ ===
def send_morning_message(context=None):
    message = random.choice(MESSAGES) + "\n\n" + random.choice(QUESTIONS)
    if context:
        context.bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        updater.bot.send_message(chat_id=CHAT_ID, text=message)

# === РАСПИСАНИЕ ДЛЯ ЕЖЕДНЕВНОЙ ОТПРАВКИ ===
def schedule_checker():
    tz = pytz.timezone("Asia/Almaty")
    sent_today = False
    while True:
        now = datetime.now(tz)
        if now.hour == 10 and now.minute == 30:
            if not sent_today:
                send_morning_message()
                sent_today = True
        elif now.hour == 8 and now.minute > 30:
            sent_today = False
        time.sleep(20)

# === ОСНОВНАЯ ЛОГИКА БОТА ===
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я готов присылать тебе вдохновение по утрам ☀️")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# === ЗАПУСК ===
if __name__ == '__main__':
    threading.Thread(target=schedule_checker, daemon=True).start()
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()
    updater.start_polling()
    updater.idle()