from telegram.ext import Updater, CommandHandler

TOKEN = '7587932544:AAFkq39PjCaul1H5EEvvOyunAyFeD1adayc'

def start(update, context):
    update.message.reply_text("안녕하세요! 텔레그램 자동 매크로 봇입니다.")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
