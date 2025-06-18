import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

# 환경 변수
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "8443"))
APP_NAME = os.getenv("APP_NAME")
TARGET_CHAT_ID = "@test999"

# 로깅
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 이미지 순서
image_files = ["test.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg"]
current_index = 0

# 자동 공지 함수
def send_notice(context):
    global current_index
    try:
        filename = image_files[current_index]
        with open(filename, "rb") as photo:
            context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=photo,
                caption=f"📢 자동 공지입니다.\n현재 이미지: {filename}"
            )
        current_index = (current_index + 1) % len(image_files)
    except Exception as e:
        logging.error(f"[오류] 이미지 전송 실패 ({filename}): {e}")

# /start 명령 처리
def start(update, context):
    update.message.reply_text("👋 안녕하세요! Webhook 기반 공지 봇이 작동 중입니다.")
    logging.info(f"/start 호출됨 - chat_id: {update.effective_chat.id}")

# 새 멤버 인삿말 전송
def welcome_new_member(update, context):
    for user in update.message.new_chat_members:
        try:
            with open("welcome.jpg", "rb") as photo:
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo,
                    caption=f"👋 {user.full_name}님, 환영합니다!"
                )
        except Exception as e:
            logging.error(f"[오류] 인삿말 이미지 전송 실패: {e}")

# 메인 함수
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # 핸들러 등록
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_new_member))

    # 스케줄러 시작
    seoul_tz = pytz.timezone("Asia/Seoul")
    scheduler = BackgroundScheduler(timezone=seoul_tz)
    scheduler.add_job(send_notice, 'interval', minutes=1, args=[updater.job_queue])
    scheduler.start()

    # Webhook 시작
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{APP_NAME}.onrender.com/{TOKEN}"
    )

    updater.idle()

if __name__ == "__main__":
    main()
