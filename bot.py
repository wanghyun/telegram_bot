import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz

# 1. 설정
TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'
TARGET_CHAT_ID = '@test999'  # 채널명
image_files = ["test.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg"]
current_index = 0

# 2. 로깅
logging.basicConfig(level=logging.INFO)

# 3. Flask 앱 생성
app = Flask(__name__)
bot = Bot(token=TOKEN)

# 4. 자동 공지 전송 함수
def send_notice():
    global current_index
    try:
        filename = image_files[current_index]
        with open(filename, "rb") as photo:
            bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=photo,
                caption=f"⏰ 자동 공지: {filename} 이미지입니다."
            )
        current_index = (current_index + 1) % len(image_files)
    except Exception as e:
        logging.error(f"[오류] 이미지 전송 실패: {e}")

# 5. /start 명령어 처리
def start(update, context):
    update.message.reply_text("🤖 안녕하세요! 자동 공지 봇입니다.")
    logging.info(f"/start 요청 - chat_id: {update.effective_chat.id}")

# 6. 새 유저 환영
def welcome(update, context):
    for user in update.message.new_chat_members:
        try:
            with open("welcome.jpg", "rb") as photo:
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo,
                    caption=f"👋 {user.full_name}님, 환영합니다!"
                )
        except Exception as e:
            logging.error(f"[오류] 환영 이미지 전송 실패: {e}")

# 7. /안전 명령어 처리
def safety_command(update, context):
    try:
        now = datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")
        if os.path.exists("sa.txt"):
            with open("sa.txt", "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = "⚠️ sa.txt 파일이 존재하지 않습니다."

        message = f"📅 현재 시각: {now}\n\n📄 안전 공지:\n{content}"
        update.message.reply_text(message)

    except Exception as e:
        logging.error(f"[오류] /안전 처리 실패: {e}")
        update.message.reply_text("⚠️ 안전 정보를 불러오는 중 오류가 발생했습니다.")

# 8. Flask에서 Webhook 처리
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# 9. 메인 시작
if __name__ == '__main__':
    # Dispatcher 등록
    from telegram.ext import Dispatcher
    dispatcher = Dispatcher(bot, None, use_context=True)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("안전", safety_command))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    # Webhook 설정
    WEBHOOK_URL = "https://telegram-bot-lcqh.onrender.com"  # Render 앱 주소
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

    # 스케줄러 시작
    scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Seoul"))
    scheduler.add_job(send_notice, 'interval', minutes=1)
    scheduler.start()

    # Flask 앱 실행
    app.run(host='0.0.0.0', port=10000)
