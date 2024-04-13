import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
# TOKEN = os.getenv('BOT_TOKEN')
TOKEN = "6589007313:AAFsKCPJl65U37dflqq8zQxhIXrkVB6DxIs"
from dbhelper import DBHelper
from test_md import test_md
db = DBHelper()
 
db.setup()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



def showRandomWord(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = db.get_random_word()
    if word:
    #  ⭐
        star = "⭐" if word[6] == 1 else ""
        
        
        message =f"""
<b>{word[0]}</b>  {star} 
<i>{word[2]}</i>

{word[3]} 

Synonyms: <i> {word[4]}</i>

<blockquote>{word[5]}</blockquote>
        """
        
        
        
   
    else:
        message = "No words found"
    return message


async def listenToInput(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "show":
        msg= showRandomWord(update, context)

    elif update.message.text == "test":
        msg= test_md
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode="HTML" )

    
    


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    start_handler = CommandHandler('start', start)
    echo_handler = CommandHandler('echo', echo)
    caps_handler = CommandHandler('caps', caps)
    
     
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)

    input_handler = MessageHandler(filters.TEXT, listenToInput)
    application.add_handler(input_handler)


    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()