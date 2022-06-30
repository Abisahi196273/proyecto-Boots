from telegram import ParseMode
from telegram import Update
import configparser
import logging
import telegram
from flask import Flask,request
from urllib3 import make_headers

import sys
sys.path.insert(0, 'C:/Domain_User/')
from get_constants import (get_user_pass)
data_login = get_user_pass()

app = Flask(__name__)

GROUP_ID=-1001221065768
TOKEN = '5553346065:AAGn7b0RLvDS7SsNNEeHOMg7YTCxovKgHPw'  #'709849553:AAEir6wHa0pFypEspyxENUJOiyEJ64aXGvg'
REQUEST_KWARGS={
    'proxy_url': 'http://proxy.sat.gob.mx:3128/',
    'urllib3_proxy_kwargs': {
        'proxy_headers': make_headers(proxy_basic_auth=data_login['domain_user']+':'+data_login['password']),
        'username': 'Abisahi2690 ',
        'password': 'cped_bot1',
    },
}

from telegram.ext import Updater,CommandHandler,MessageHandler,filters,CallbackContext
updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher
bot = updater.bot

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def whatever_chatbot_funtion():
    dispatcher.add_handler(CommandHandler('start',start_handler))
if __name__=="__main__":
    app.run(debug=True)
# def start(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text="This is a Test, No reaction bot, only notify thanks")
#
# from telegram.ext import CommandHandler
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
# chat_list = updater.bot.get_updates()
# for chat in chat_list:
#     chat_id = chat.message.chat_id
#     print(chat_id)
# -1001406198751
#updater.start_polling()

def send_message(text):
    bot.send_message(chat_id=GROUP_ID, text=text,parse_mode = ParseMode.HTML)

def send_file(file_path):
    with open(file_path, 'rb') as f:
        bot.send_document(GROUP_ID, document=f)


