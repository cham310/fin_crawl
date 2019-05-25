import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

cham_token = ''

cham = telegram.Bot(token=cham_token)

print('start telegram chat bot')


def get_message(bot, update) :

    if update.message.text == "적금":
        update.message.reply_text("뭘 좀 아시는군요..")
    elif update.message.text == "사랑해":
        update.message.reply_text("나도 사랑해 키키키 여창쓰 최고")

    elif update.message
    else:
        update.message.reply_text("채민이 시킨 말을 하세요!")

updater = Updater(cham_token)

message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()