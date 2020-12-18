import sqlite3
import random
import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = os.environ.get('TOKEN')

logging.basicConfig(filename='loggiorgio.txt', format= "%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()

def giorgiopls(update: Update, context: CallbackContext) -> None:
    try:
        sqliteConnection = sqlite3.connect('Songs.db')
        cursor = sqliteConnection.cursor()
        logger.info("initializing..")
    except:
        logger.error("Error while initializing", exc_info=True)
    try:
        cursor.execute("SELECT * from Songs")
        records = cursor.fetchall()
        logger.info("Getting the number of records")
    except:
        logger.error("Error while getting records", exc_info=True)
    totalrows = (len(records))  #lets get the total number of rows of the db
    Id = random.randint(1, totalrows)
    try:
        cursor.execute("SELECT * from Songs where Id = ?", (Id,))
        record = cursor.fetchone()[3] #retrive the url of the song
        response = record
        logger.info("Retrieving the URL")
    except:
        logger.error("Error while queryng DB", exc_info=True)
    cursor.close()
    try:
        update.message.reply_text(response)
        logger.info("Video sent successfully")
    except:
        logger.error("Error while sending message", exc_info=True)

def aiuto(update, context):
    update.message.reply_text("I comandi possibili sono: \n /giorgiopls per una canzone random \n /about per info su questo bot \n /aiuto per la lista dei comandi")

def about(update, context):
    update.message.reply_text("Fatto con amore da flyingwonton, https://github.com/flyingwonton/giorgiopoibot")

def bot():
    #"""Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("aiuto", aiuto))
    dispatcher.add_handler(CommandHandler("about", about))
    #let's allow some variation
    dispatcher.add_handler(CommandHandler("giorgiopls", giorgiopls))
    dispatcher.add_handler(CommandHandler("giorgioplz", giorgiopls))
    dispatcher.add_handler(CommandHandler("giorgioplease", giorgiopls))
    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    bot()