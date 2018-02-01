import sqlite3
from sqlite3 import Error

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from ConfigParser import SafeConfigParser
from emoji import emojize

#emojis: https://www.webpagefx.com/tools/emoji-cheat-sheet/

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
    update.message.reply_text(emojize("fer servir la comanda /pregunta"))

def pregunta(bot, update):
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

    statsdb = config.get('bot', 'statsfile')
    statsconn = create_connection(statsdb)
    statscur = statsconn.cursor()
    statscur.execute("SELECT * FROM stats where id_user=? LIMIT 1", (query.from.id,))

    users = statscur.fetchall()

    # si no existeix, crear a 0
    if len(users) == 0:
      statscur.execute("INSERT INTO stats VALUES ...")

    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM preguntes WHERE pregunta=? LIMIT 1", (query.message.text,))

    rows = cur.fetchall()

    print query

    for row in rows:
        response=row[1]+"\n\n"
	
	for i in range(2,6):
		if len(row[i]) > 0:
			lletra=chr(ord('a') + i-2)
			if lletra == row[6]:
				response+=lletra+") "+row[i]+"  :white_check_mark:\n"
			else:
				if lletra == query.data:
					response+=lletra+") "+row[i]+" :x:\n"
				else:
					response+=lletra+") "+row[i]+"\n"
					
	bot.edit_message_text(text=emojize(response, use_aliases=True),
        	                chat_id=query.message.chat_id,
				message_id=query.message.message_id)
    pregunta(update)


config = SafeConfigParser()
config.read('testbot.config')

BOT_TOKEN = config.get('bot', 'token')

updater = Updater(token=BOT_TOKEN)

dp = updater.dispatcher

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('pregunta', pregunta))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()

updater.idle()
