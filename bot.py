from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import pytz

# 1. 봇 토큰과 채팅 대상 설정
TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'
TARGET_CHAT_ID = 2059077213

# 2. 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 3. 이미지 목록 및 인덱스
image_files = ["test.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg"]
current_index = 0  # 전역 인덱스

# 4. 공지 전송 함수 (이미지 순환)
def send_notice(bot):
    global current_index
    try:
        filename = image_files[current_index]
        with open(filename, "rb") as photo:
            bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=photo,
                caption=f"⏰ 자동 공지입니다. 5분마다 이미지가 순서대로 전송됩니다.\n지금은: {filename}"
            )
        current_index = (current_index + 1) % len(image_files)  # 순환 처리
    except Exception as e:
        print(f"[오류] 이미지 전송 실패 ({filename}): {e}")

# 5. /start 명령 처리
def start(update, context):
    update.message.reply_text("안녕하세요! 자동 이미지 공지 봇이 작동 중입니다.")
    print(f"[INFO] /start 요청 - chat_id: {update.effective_chat.id}")

# 6. 메인 실행 함수
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    # 스케줄러 설정 (한국 시간대 기준)
    seoul_tz = pytz.timezone("Asia/Seoul")
    scheduler = BackgroundScheduler(timezone=seoul_tz)
    scheduler.add_job(send_notice, 'interval', minutes=1, args=[updater.bot])
    scheduler.start()

    updater.start_polling()
    updater.idle()

# 7. 실행
if __name__ == '__main__':
    main()
