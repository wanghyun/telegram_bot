from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import pytz

# 1. 텔레그램 봇 토큰과 대상 chat_id
TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'
TARGET_CHAT_ID = 2059077213  # 본인 채팅방 ID

# 2. 로깅 설정 (Render 로그 확인용)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 3. 자동 공지 전송 함수
def send_notice(context):
    try:
        with open("test.jpg", "rb") as photo:
            context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=photo,
                caption="⏰ 자동 공지입니다. 5분마다 전송됩니다.\n이 이미지는 함께 첨부된 예시입니다."
            )
    except Exception as e:
        print(f"[오류] 이미지 전송 실패: {e}")

# 4. /start 명령어 처리 함수
def start(update, context):
    update.message.reply_text("안녕하세요! 자동 공지 봇이 작동 중입니다.\n이 채팅방 ID는 이미 등록되어 있습니다.")
    print(f"[INFO] /start 요청 - chat_id: {update.effective_chat.id}")

# 5. 메인 함수
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # /start 명령어 등록
    dispatcher.add_handler(CommandHandler("start", start))

    # 6. APScheduler 설정: 한국 시간 기준 5분마다 실행
    seoul_tz = pytz.timezone("Asia/Seoul")
    scheduler = BackgroundScheduler(timezone=seoul_tz)
    scheduler.add_job(send_notice, 'interval', minutes=1, args=[updater.job_queue])
    scheduler.start()

    # 7. 봇 실행
    updater.start_polling()
    updater.idle()

# 8. 시작
if __name__ == '__main__':
    main()
