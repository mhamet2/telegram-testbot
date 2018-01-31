import sqlite3
from sqlite3 import Error

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from ConfigParser import SafeConfigParser


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def start(bot, update):
    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM  preguntes ORDER BY RANDOM() LIMIT 1")

    rows = cur.fetchall()

    for row in rows:

	    keyboard = [[InlineKeyboardButton(row[2], callback_data='a')],
        	        [InlineKeyboardButton(row[3], callback_data='b')],
                	[InlineKeyboardButton(row[4], callback_data='c')],
	                [InlineKeyboardButton(row[5], callback_data='d')]]

	    reply_markup = InlineKeyboardMarkup(keyboard)

	    update.message.reply_text(row[1], reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM preguntes WHERE pregunta=? LIMIT 1", (query.message.text,))

    rows = cur.fetchall()

    for row in rows:
	print row
        response=row[1]+"\n"+row[2]+"\n"+row[3]
        if row[6] == query.data:
		result="CORRECTE"
	else:
		result="INCORRECTE"
	response+=result
	#bot.edit_message_text(text="Selected option: {} {}".format(query.data,query.message.text),
	bot.edit_message_text(text=response,
        	                chat_id=query.message.chat_id,
				message_id=query.message.message_id)


config = SafeConfigParser()
config.read('perbot.config')

BOT_TOKEN = config.get('bot', 'token')

updater = Updater(token=BOT_TOKEN)

dp = updater.dispatcher

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()

updater.idle()
