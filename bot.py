from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import pytz

# 1. 봇 설정
TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'
TARGET_CHAT_ID = 2059077213  # 개인, 채널, 그룹 등

# 2. 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 3. 자동 공지 이미지 순서
image_files = ["test.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg"]
current_index = 0  # 현재 전송할 이미지 인덱스

# 4. 공지 전송 함수
def send_notice(bot):
    global current_index
    try:
        filename = image_files[current_index]
        with open(filename, "rb") as photo:
            bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=photo,
                caption=f"⏰ 자동 공지입니다. 1분마다 이미지가 순서대로 전송됩니다.\n지금은: {filename}"
            )
        current_index = (current_index + 1) % len(image_files)
    except Exception as e:
        print(f"[오류] 이미지 전송 실패 ({filename}): {e}")

# 5. /start 명령 처리
def start(update, context):
    update.message.reply_text("안녕하세요! 자동 공지 봇이 작동 중입니다.")
    print(f"[INFO] /start 요청 - chat_id: {update.effective_chat.id}")

# 6. 새 유저 인삿말 전송
def welcome_new_member(update, context):
    for user in update.message.new_chat_members:
        try:
            with open("welcome.jpg", "rb") as photo:
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo,
                    caption=f"👋 {user.full_name}님, 어서 오세요!\n이 채팅방에 오신 것을 환영합니다!"
                )
        except Exception as e:
            print(f"[오류] 인삿말 이미지 전송 실패: {e}")

# 7. 메인 함수
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # 명령 및 이벤트 핸들러 등록
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_new_member))

    # 1분마다 자동 공지 스케줄러 설정
    seoul_tz = pytz.timezone("Asia/Seoul")
    scheduler = BackgroundScheduler(timezone=seoul_tz)
    scheduler.add_job(send_notice, 'interval', minutes=3, args=[updater.bot])
    scheduler.start()

    # 봇 시작
    updater.start_polling()
    updater.idle()

# 8. 실행
if __name__ == '__main__':
    main()
