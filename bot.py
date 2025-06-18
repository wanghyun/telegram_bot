from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import pytz
import os

# ==== 기본 설정 ====
TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'
TARGET_CHAT_ID = '@test999'  # 채널 username
APP_URL = 'https://telegram-bot-lcqh.onrender.com'  # Render에서 제공된 도메인

image_files = ["test.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg"]
current_index = 0

# ==== Flask 앱 ====
app = Flask(__name__)
bot = Bot(token=TOKEN)

# ==== 로깅 ====
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# ==== 디스패처 설정 ====
dispatcher = Dispatcher(bot, None, use_context=True)

# ==== 핸들러 ====
def start(update, context):
    update.message.reply_text("🤖 안녕하세요! 자동 공지 봇이 작동 중입니다.")
    logging.info(f"[INFO] /start 요청 - chat_id: {update.effective_chat.id}")

def welcome(update, context):
    for user in update.message.new_chat_members:
        with open("welcome.jpg", "rb") as photo:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption=f"👋 {user.full_name}님, 환영합니다!"
            )

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

# ==== 이미지 자동 공지 ====
def send_notice():
    global current_index
    try:
        filename = image_files[current_index]
        with open(filename, "rb") as photo:
            bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=photo,
                caption=f"🗓️ 자동 공지 이미지입니다.\n파일명: {filename}"
            )
        current_index = (current_index + 1) % len(image_files)
    except Exception as e:
        logging.error(f"[오류] 이미지 전송 실패: {e}")

# ==== 스케줄러 시작 ====
scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Seoul"))
scheduler.add_job(send_notice, 'interval', minutes=1)
scheduler.start()

# ==== Webhook 엔드포인트 ====
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

# ==== 서버 기본 라우팅 ====
@app.route('/')
def index():
    return '✅ Telegram Webhook 서버 작동 중입니다.'

# ==== Webhook 등록 ====
def set_webhook():
    webhook_url =_
