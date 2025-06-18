from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# 텔레그램 봇 토큰과 chat_id 설정
TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'
TARGET_CHAT_ID = 2059077213

# 로깅 설정
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 자동 공지 전송 함수 (이미지 + 텍스트)
def send_notice(context):
    with open("test.jpg", "rb") as photo:
        context.bot.send_photo(
            chat_id=TARGET_CHAT_ID,
            photo=photo,
            caption="⏰ 자동 공지입니다. 5분마다 전송됩니다.\n이 이미지는 함께 첨부된 예시입니다."
        )

# /start 명령어 처리
def start(update, context):
    update.message.reply_text("안녕하세요! 자동 공지 봇이 작동 중입니다.\n이 채팅방 ID는 이미 등록되어 있습니다.")

# 메인 함수
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # /start 명령어 등록
    dispatcher.add_handler(CommandHandler("start", start))

    # APScheduler로 5분마다 공지 실행
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_notice, 'interval', minutes=5, args=[updater.job_queue])
    scheduler.start()

    # 봇 실행
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
