import asyncio
import logging
import traceback

import telegram
import gdoc
import stats

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
loggerhttpx = logging.getLogger('httpx')
loggerhttpx.setLevel('WARNING') #now it doesn't shit every heartbeat

token = None
with open('token') as f: #TODO: handle lack of token file
    token = f.readline()[0:-1] #TODO crop the endline symbol out of the token properly, this is fragile
#print(token)

helpfile = None
with open ('help.md',encoding='utf-8') as f:
    helpfile = f.read()
#print(helpfile)

active_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Mew, do a /man, mew mew")
    
async def h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="h")
    
def split_transaction(update):
    payload = update.message.text
    split = payload.split('\n')
    obj = split[1]
    sum_ = float(split[2]) #TODO make an error handler
    #sum_ = split[2]
    cat = ''
    place = ''
    user = gdoc.usernames[update.message.chat.username]
    if len(split)>3:
        cat = split[3]
    if len(split)>4:
        place = split[4]
    return obj, sum_, cat, user, place

async def income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    obj, sum_, cat, user, place = split_transaction(update)
    gdoc.add_record(gdoc.sheet, 0, obj, sum_, cat, user ,place)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Income registered")

async def spend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    obj, sum_, cat, user, place = split_transaction(update)
    gdoc.add_record(gdoc.sheet, 1, obj, sum_, cat, user ,place)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Spend registered")

async def man(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=helpfile)
    
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(gdoc.categories)) #TODO: output this nicely
    
async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payload = update.message.text
    split = payload.split('\n')
    year = int(split[1])
    if(len(split)>2):
        month = int(split[2])
        retval = stats.get_stats_month(gdoc.userids[update.message.chat.username], month, year)
    else:
        retval = stats.get_stats_year(gdoc.userids[update.message.chat.username], year)
    await context.bot.send_document(chat_id=update.effective_chat.id, document='Income.png')
    await context.bot.send_document(chat_id=update.effective_chat.id, document='Spend.png') #TODO delete the pics after send
    await context.bot.send_message(chat_id=update.effective_chat.id, text=retval)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    # https://docs.python-telegram-bot.org/en/v21.6/examples.errorhandlerbot.html
    # https://docs.python.org/3/library/logging.html#logging.Logger.debug
    logger.error("Exception while handling an update:", exc_info=context.error)
    #logger.error('the error was above')
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    await context.bot.send_message(chat_id=update.effective_chat.id,text=str(context.error))
    

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler('h',h))
    application.add_handler(CommandHandler('income',income))
    application.add_handler(CommandHandler('spend',spend))
    application.add_handler(CommandHandler('man',man))
    application.add_handler(CommandHandler('help',man))
    application.add_handler(CommandHandler('test',test))
    application.add_handler(CommandHandler('categories',cat))
    application.add_handler(CommandHandler('cat',cat))
    application.add_handler(CommandHandler('stats',stat))
    
    application.add_error_handler(error_handler)
    
    application.run_polling()