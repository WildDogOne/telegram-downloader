from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import requests
import os
from creds import TOKEN

def start(update: Update, context):
    update.message.reply_text('Hello! Please send me a URL of an image and I will download and send it back to you.')

def handle_message(update: Update, context):
    url = update.message.text
    response = requests.get(url)
    
    if response.status_code == 200:
        with open("image.jpg", 'wb') as f:
            f.write(response.content)
            
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('image.jpg', 'rb'))
    else:
        update.message.reply_text('Failed to download the image. Please check the URL.')

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
    dispatcher.add_handler(message_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()

