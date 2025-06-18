from flask import Flask, request
import telegram
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import os

# === 설정 ===
TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'
APP_NAME = 'srv-d1940fvdiees73ag06k0'  # Render 서비스 이름 (도메인 부분)
CHAT_ID = '@test999'  # 채널, 그룹, 개인

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# === 이미지 순서 및 인덱스
image_files = ["test.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg"]
current_index = 0

# === 공지 전송 함수
def send_notice():
    global current_index
    try:
        filename = image_files[current_index]
        with open(filename, 'rb') as img:
            bot.send_photo(
                chat_id=CHAT_ID,
                photo=img,
                caption=f"📢 자동 공지: {filename}"
            )
        current_index = (current_index + 1) % len(image_files)
    except Exception as e:
        print(f"[오류] 공지 전송 실패 ({filename}): {e}")

# === Webhook 메시지 처리
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        if update.message.new_chat_members:
            for user in update.message.new_chat_members:
                try:
                    with open("welcome.jpg", "rb") as img:
                        bot.send_photo(
                            chat_id=update.effective_chat.id,
                            photo=img,
                            caption=f"👋 {user.full_name}님 환영합니다!"
                        )
                except Exception as e:
                    print(f"[오류] 환영 이미지 전송 실패: {e}")
        elif update.message.text:
            bot.send_message(chat_id=update.effective_chat.id, text="🤖 자동 공지 봇입니다.")

    return 'ok'

# === 메인 함수: 스케줄러 시작 및 Webhook 등록
if __name__ == '__main__':
    scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Seoul'))
    scheduler.add_job(send_notice, 'interval', minutes=1)
    scheduler.start()

    # Render 도메인에 Webhook 등록
    bot.set_webhook(f"https://{APP_NAME}.onrender.com/{TOKEN}")

    # Flask 앱 실행
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
