from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import os
import logging
import pytz

# ====================== 기본 설정 ======================
TOKEN = "7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc"
APP_NAME = "telegram-bot-lcqh"  # Render 서비스 이름 (URL 앞부분)
WEBHOOK_URL = f"https://{APP_NAME}.onrender.com/{TOKEN}"
TARGET_CHAT_ID = "@test999"  # 채널 사용자명
image_files = ["test.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg"]
current_index = 0

bot = Bot(token=TOKEN)

# ====================== Flask 앱 ======================
app = Flask(__name__)

# ====================== 로깅 ======================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ====================== 핸들러 함수 ======================
def start(update, context):
    update.message.reply_text("안녕하세요! 자동 공지 봇입니다.")
    logger.info(f"/start 요청 - chat_id: {update.effective_chat.id}")

def welcome(update, context):
    for user in update.message.new_chat_members:
        try:
            with open("welcome.jpg", "rb") as photo:
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo,
                    caption=f"👋 {user.full_name}님, 어서 오세요!"
                )
        except Exception as e:
            logger.error(f"[오류] 환영 이미지 전송 실패: {e}")

def safety(update, context):
    try:
        with open("sa.txt", "r") as f:
            content = f.read()
    except:
        content = "[경고] sa.txt 파일이 없습니다."
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"📅 현재 시각: {now}\n📄 안전 내용:\n{content}"
    update.message.reply_text(message)

def send_notice():
    global current_index
    try:
        filename = image_files[current_index]
        with open(filename, "rb") as photo:
            bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=photo,
                caption=f"📢 자동 공지입니다: {filename}"
            )
        current_index = (current_index + 1) % len(image_files)
    except Exception as e:
        logger.error(f"[오류] 공지 이미지 전송 실패 ({filename}): {e}")

# ====================== Flask 라우터 ======================
@app.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "Telegram Webhook Bot 작동 중!", 200

# ====================== 메인 함수 ======================
def main():
    global dispatcher

    dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(".*안전.*"), safety))

    # 스케줄러 설정
    seoul_tz = pytz.timezone("Asia/Seoul")
    scheduler = BackgroundScheduler(timezone=seoul_tz)
    scheduler.add_job(send_notice, "interval", minutes=1)
    scheduler.start()

    # Webhook 등록
    bot.set_webhook(WEBHOOK_URL)
    logger.info(f"[설정] Webhook 설정 완료: {WEBHOOK_URL}")

    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()
