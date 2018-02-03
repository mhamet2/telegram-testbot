import sqlite3
import os.path
import logging

from sqlite3 import Error
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from ConfigParser import SafeConfigParser
from emoji import emojize

#emojis: https://www.webpagefx.com/tools/emoji-cheat-sheet/

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def showpenis(bot, update):
    if os.path.isfile('./img/29.jpg'):
	bot.send_photo(chat_id=update.message.chat_id, photo=open('./img/29.jpg', 'rb'))

def stats(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    statsdb = config.get('bot', 'statsfile')
    statsconn = create_connection(statsdb)
    statscur = statsconn.cursor()
    statscur.execute("SELECT id,id_user,ok,failed FROM stats WHERE id_user=? LIMIT 1", (user_id,))

    users = statscur.fetchall()

    if len(users)<=0:
        update.message.reply_text(emojize("No hi ha dades"), use_aliases=True)
    else:
        for user in users:
            update.message.reply_text(emojize(" :white_check_mark: "+str(user[2])+"\n :x: "+str(user[3]), use_aliases=True))

def resetstats(bot, update):
    user_id = update.message.from_user.id

    statsdb = config.get('bot', 'statsfile')
    statsconn = create_connection(statsdb)
    statscur = statsconn.cursor()
    statscur.execute("DELETE FROM stats WHERE id_user=?", (user_id,))

    statsconn.commit()

    update.message.reply_text(emojize("estadistiques resetejades", use_aliases=True))

def start(bot, update):
    update.message.reply_text(emojize("fer servir la comanda /pregunta", use_aliases=True))

def pregunta(bot, update):
    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT id,pregunta,resposta_a,resposta_b,resposta_c,resposta_d,resposta_correcte FROM  preguntes ORDER BY RANDOM() LIMIT 1")

    rows = cur.fetchall()


    for row in rows:
            for ext in [ 'jpg', 'png' ]:
                if os.path.isfile('./img/'+str(row[0])+'.'+ext):
                    #bot.send_photo(chat_id=chat_id, photo=open('tests/test.png', 'rb'))
                    bot.send_photo(chat_id=update.message.chat_id, photo=open('./img/'+str(row[0])+'.'+ext, 'rb'))

            keyboard = [[InlineKeyboardButton(row[2], callback_data='a')],
                        [InlineKeyboardButton(row[3], callback_data='b')],
                        [InlineKeyboardButton(row[4], callback_data='c')],
                        [InlineKeyboardButton(row[5], callback_data='d')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(row[1], reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    user_id = query.from_user.id
    display_name = query.from_user.first_name

    # print query

    statsdb = config.get('bot', 'statsfile')
    statsconn = create_connection(statsdb)
    statscur = statsconn.cursor()
    statscur.execute("SELECT id,id_user,ok,failed FROM stats WHERE id_user=? LIMIT 1", (user_id,))

    users = statscur.fetchall()

    # si no existeix, crear a 0
    if len(users) == 0:
      statscur = statsconn.cursor()
      statscur.execute("INSERT INTO stats(id_user,ok,failed,display_name) VALUES (?,0,0,?)",(user_id,display_name,))
      statsconn.commit()
      statscur = statsconn.cursor()
      statscur.execute("SELECT id,id_user,ok,failed FROM stats WHERE id_user=? LIMIT 1", (user_id,))
      users = statscur.fetchall()

    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT id,pregunta,resposta_a,resposta_b,resposta_c,resposta_d,resposta_correcte,display_name FROM preguntes WHERE pregunta=? LIMIT 1", (query.message.text,))

    rows = cur.fetchall()

    #print query

    for row in rows:
        response=row[1]+"\n\n"
    	encertada=True
    	for i in range(2,6):
    		if len(row[i]) > 0:
    			lletra=chr(ord('a') + i-2)
    			if lletra == row[6]:
    				response+=lletra+") "+row[i]+"  :white_check_mark:\n"
    			else:
    				if lletra == query.data:
    					response+=lletra+") "+row[i]+" :x:\n"
    					encertada=False
    				else:
    					response+=lletra+") "+row[i]+"\n"

    	statscur = statsconn.cursor()

    	if encertada:
    		statscur.execute("UPDATE stats SET ok = ok + 1 WHERE id_user=?",(user_id,))
    	else:
    		statscur.execute("UPDATE stats SET failed = failed + 1 WHERE id_user=?",(user_id,))

        if row[8]!=display_name:
    	       statscur.execute("UPDATE stats SET display_name = ? WHERE id_user=?",(display_name, user_id,))
    	statsconn.commit()

    	bot.edit_message_text(text=emojize(response, use_aliases=True),
            	                chat_id=query.message.chat_id,
    	                        message_id=query.message.message_id)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

config = SafeConfigParser()
config.read('testbot.config')

BOT_TOKEN = config.get('bot', 'token')

updater = Updater(token=BOT_TOKEN)

dp = updater.dispatcher

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('pregunta', pregunta))
updater.dispatcher.add_handler(CommandHandler('stats', stats))
updater.dispatcher.add_handler(CommandHandler('resetstats', resetstats))
updater.dispatcher.add_handler(CommandHandler('kill', showpenis))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()

updater.idle()
