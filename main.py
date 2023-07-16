import asyncio
import logging
import telegram
import gdoc
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

token = None
with open('token') as f: #TODO: handle lack of token file
    token = f.readline()[0:-1] #TODO crop the endline symbol out of the token properly, this is fragile
#print(token)

active_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Mew, do a /man, mew mew")
    
async def h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="h")
    
async def income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    string = update.message.text
    split = string.split('\n')
    obj = split[1]
    #sum_ = float(split[2])
    sum_ = split[2]
    cat = ''
    place = ''
    user = gdoc.usernames[update.message.chat.username]
    if len(split)>3:
        cat = split[3]
    if len(split)>4:
        place = split[4]
    gdoc.add_record(gdoc.sheet, 0, obj, sum_, cat, user ,place)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Income registered")

async def spend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    string = update.message.text
    split = string.split('\n')
    obj = split[1]
    #sum_ = float(split[2])
    sum_ = split[2]
    cat = ''
    place = ''
    user = gdoc.usernames[update.message.chat.username]
    if len(split)>3:
        cat = split[3]
    if len(split)>4:
        place = split[4]
    gdoc.add_record(gdoc.sheet, 1, obj, sum_, cat, user ,place)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Spend registered")

async def man(update: Update, context: ContextTypes.DEFAULT_TYPE): #TODO: make a man
    await context.bot.send_message(chat_id=update.effective_chat.id, text="h")
    
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler('h',h))
    application.add_handler(CommandHandler('income',income))
    application.add_handler(CommandHandler('spend',spend))
    application.add_handler(CommandHandler('man',man))
    application.add_handler(CommandHandler('test',test))
    
    application.run_polling()