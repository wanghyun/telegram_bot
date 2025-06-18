from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import logging
import os
from datetime import datetime

# 1. 설정
TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'
TARGET_CHAT_ID = '@test999'  # 채널 아이디
APP_NAME = 'telegram-bot-lcqh'  # Render 앱 이름 (URL 참고)
URL = f'https://{APP_NAME}.onrender.com'  # Webhook URL

image_files = ["test.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg"]
current_index = 0

# 2. Flask 앱 및 봇 인스턴스 생성
app = Flask(__name__)
bot = Bot(token=TOKEN)

# 3. Dispatcher 구성
dispatcher = Dispatcher(bot, None, workers=1, use_context=True)

# 4. 공지 전송 함수
def send_notice():
    global current_index
    try:
        filename = image_files[current_index]
        with open(filename, "rb") as photo:
            bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=photo,
                caption=f"📢 자동 공지입니다 (이미지: {filename})"
            )
        current_index = (current_index + 1) % len(image_files)
    except Exception as e:
        print(f"[오류] 공지 전송 실패: {e}")

# 5. /safety 명령어 처리
def safety_command(update, context):
    try:
        with open("sa.txt", "r", encoding="utf-8") as file:
            content = file.read()
        today = datetime.now().strftime("%Y-%m-%d")
        message = f"📅 오늘 날짜: {today}\n📄 안전 정보:\n{content}"
        update.message.reply_text(message)
    except Exception as e:
        update.message.reply_text(f"⚠️ 파일 읽기 오류: {e}")

# 6. 한글 /안전 명령어 메시지 처리
def message_handler(update, context):
    text = update.message.text.strip()
    if text == "/안전":
        safety_command(update, context)

# 7. 핸들러 등록
dispatcher.add_handler(CommandHandler("safety", safety_command))
dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'^/안전$'), message_handler))

# 8. Webhook 설정 엔드포인트
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

# 9. 홈 엔드포인트 (테스트용)
@app.route('/')
def index():
    return 'Bot is running!'

# 10. Webhook 등록
def set_webhook():
    webhook_url = f'{URL}/{TOKEN}'
    success = bot.set_webhook(url=webhook_url)
    print(f"[설정] Webhook 설정 완료: {webhook_url}" if success else "[오류] Webhook 설정 실패")

# 11. 스케줄러 시작
def start_scheduler():
    seoul = pytz.timezone("Asia/Seoul")
    scheduler = BackgroundScheduler(timezone=seoul)
    scheduler.add_job(send_notice, 'interval', minutes=1)
    scheduler.start()

# 12. 실행
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    set_webhook()
    start_scheduler()
    app.run(host='0.0.0.0', port=10000)
