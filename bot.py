from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# 1. 텔레그램 봇 토큰
TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'

# 2. 공지 보낼 대상 chat_id
TARGET_CHAT_ID = 2059077213

# 3. 로깅 설정 (Render나 콘솔에서 로그 확인용)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 4. 자동 공지 함수 (5분마다 실행)
def send_notice(context):
    context.bot.send_message(chat_id=TARGET_CHAT_ID, text="⏰ 자동 공지입니다. 5분마다 전송됩니다.")

# 5. /start 명령 처리 함수
def start(update, context):
    update.message.reply_text("안녕하세요! 자동 공지 봇이 작동 중입니다.\n이 채팅방 ID는 이미 등록되어 있습니다.")

# 6. 메인 함수
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # /start 핸들러 등록
    dispatcher.add_handler(CommandHandler("start", start))

    # APScheduler: 5분마다 공지 전송
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_notice, 'interval', minutes=5, args=[updater.job_queue])
    scheduler.start()

    # 봇 실행
    updater.start_polling()
    updater.idle()

# 7. 프로그램 시작점
if __name__ == '__main__':
    main()
