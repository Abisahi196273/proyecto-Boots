from telegram import ParseMode
from urllib3 import make_headers
import telegram
import datetime, pytz
#import ws_bot_web_scraping

import sys
sys.path.insert(0, 'C:/Domain_User/')
from gets_constants import get_user_pass
data_login = get_user_pass()

GROUP_ID = -1001422033185
TOKEN = '5525066415:AAFKo8v0MtzL30mCwqRQOUCMm_cRsOSU808'
REQUEST_KWARGS = {
    'proxy_url': 'http://proxy.sat.gob.mx:3128/',
    'urllib3_proxy_kwargs': {
        'proxy_headers': make_headers(proxy_basic_auth=data_login['domain_user']+':'+data_login['password']),

    },
}
from telegram.ext import Updater,MessageHandler,CommandHandler
updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS,use_context=True)
dispatcher = updater.dispatcher
print("This Bot started")
bot = updater.bot

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
def start(update,bot):
    bot.send_message(chat_id=update.message.chat_id, text="ON-OFF THIS IS A BOT")
    

from telegram.ext import CommandHandler
start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)

"""chat_list = updater.bot.get_updates()
for chat in chat_list:
    chat_id = chat.message.chat_id
    print(chat_id)"""
#Pones a correr el bot
updater.start_polling()
updater.idle()

def send_message(text):
    bot.send_message(chat_id=GROUP_ID, text=text,parse_mode = ParseMode.HTML)

def send_file(file_path):
    with open(file_path, 'rb') as f:
        bot.send_document(GROUP_ID, document=f)
#send_message(' Wellcome to Send_bot is <b>!bot send_messages ........!!</b>')
#send_file('C:/Users/MAMA909P/Documents/python/final.txt')

#DEFINIR EL PARO DEL BOT UNA VEZ TERMINADO LOS PROCESOS






