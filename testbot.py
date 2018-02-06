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
    if os.path.isfile('./preguntes/29.jpg'):
	bot.send_photo(chat_id=update.message.chat_id, photo=open('./preguntes/29.jpg', 'rb'))

def showversion(bot, update):
    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT count(*) AS count FROM  preguntes")

    rows = cur.fetchall()

    if len(rows)<=0:
        update.message.reply_text(emojize("No hi ha dades"), use_aliases=True)
    else:
        for row in rows:
            update.message.reply_text(emojize("Total: "+str(row['count'])), use_aliases=True)
    conn.close()

def ranking(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    statsdb = config.get('bot', 'statsfile')
    statsconn = create_connection(statsdb)
    statsconn.row_factory = sqlite3.Row
    statscur = statsconn.cursor()
    statscur.execute("SELECT id,id_user,ok,failed,display_name FROM stats ORDER BY ok DESC, failed ASC LIMIT 10")

    users = statscur.fetchall()

    if len(users)<=0:
        update.message.reply_text(emojize("No hi ha dades"), use_aliases=True)
    else:
        ranking = []
        ranking.append("ranking:\n\n")
        for user in users:
            if (user['display_name'] is not None and len(user['display_name']) > 0 and user['ok']+user['failed'] > 0):
                ranking.append(''+user['display_name']+" :white_check_mark: "+str(user['ok'])+" :x: "+str(user['failed'])+"\n")
        update.message.reply_text(emojize(''.join(ranking), use_aliases=True))
    statsconn.close()

def stats(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    statsdb = config.get('bot', 'statsfile')
    statsconn = create_connection(statsdb)
    statsconn.row_factory = sqlite3.Row
    statscur = statsconn.cursor()
    statscur.execute("SELECT id,id_user,ok,failed FROM stats WHERE id_user=? LIMIT 1", (user_id,))

    users = statscur.fetchall()

    if len(users)<=0:
        update.message.reply_text(emojize("No hi ha dades"), use_aliases=True)
    else:
        for user in users:
            update.message.reply_text(emojize(" :white_check_mark: "+str(user['ok'])+"\n :x: "+str(user['failed']), use_aliases=True))
    statsconn.close()

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

def getWherePregunta(stats):

    tema = stats[6]
    examen = stats[7]
    modalitat = stats[8]

    return "WHERE modalitat=\""+modalitat+"\""

def setTema(bot, update):
    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT tema FROM preguntes WHERE tema is not NULL and tema != '' GROUP BY tema ORDER BY tema")

    temes = cur.fetchall()

    count=0
    keyboard_buttons=[]
    for tema in temes:
        keyboard_buttons.append([InlineKeyboardButton(tema, callback_data='t-'+str(count)+'-0')])
        count=count+1
        # update.message.reply_text(emojize(tema['tema'], use_aliases=True))

    reply_markup = InlineKeyboardMarkup(keyboard_buttons)
    update.message.reply_text('selecciona tema:', reply_markup=reply_markup)


    conn.close()

def setModalitat(bot, update):
    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT modalitat FROM preguntes WHERE modalitat is not NULL and modalitat != '' GROUP BY modalitat")

    temes = cur.fetchall()

    for tema in temes:
        update.message.reply_text(emojize(tema['modalitat'], use_aliases=True))

    conn.close()

def setExamen(bot, update):
    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT examen FROM preguntes WHERE examen is not NULL and examen != '' GROUP BY examen")

    temes = cur.fetchall()

    for tema in temes:
        update.message.reply_text(emojize(tema['examen'], use_aliases=True))

    conn.close()


def pregunta(bot, update):
    user_id = update.message.from_user.id
    display_name = ''

    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    statsdb = config.get('bot', 'statsfile')
    statsconn = create_connection(statsdb)
    statsconn.row_factory = sqlite3.Row
    statscur = statsconn.cursor()
    statscur.execute("SELECT id,id_user,ok,failed,display_name,offset_preguntes,tema,examen,modalitat FROM stats WHERE id_user=? LIMIT 1", (user_id,))

    users = statscur.fetchall()

    # si no existeix, crear a 0
    if len(users) == 0:
      statscur = statsconn.cursor()
      statscur.execute("INSERT INTO stats(id_user,ok,failed,display_name,offset_preguntes) VALUES (?,0,0,?,0)",(user_id,display_name,))
      statsconn.commit()
      statscur = statsconn.cursor()
      statscur.execute("SELECT id,id_user,ok,failed,display_name,offset_preguntes,tema,examen,modalitat FROM stats WHERE id_user=? LIMIT 1", (user_id,))
      users = statscur.fetchall()

    for user in users:
        stats_display_name = user['display_name']
        offset_preguntes = user['offset_preguntes']
        condicio_pregunta = getWherePregunta(user)

    sql_preguntes="SELECT id,pregunta,resposta_a,resposta_b,resposta_c,resposta_d,resposta_correcte FROM preguntes "+condicio_pregunta+" LIMIT 1 OFFSET ?"

    cur.execute(sql_preguntes,(offset_preguntes,))

    rows = cur.fetchall()

    if len(rows) > 0:
        offset_preguntes+=1
    else:
        offset_preguntes=0
        cur = conn.cursor()
        cur.execute("SELECT id,pregunta,resposta_a,resposta_b,resposta_c,resposta_d,resposta_correcte FROM  preguntes LIMIT 1 OFFSET ?",(offset_preguntes,))

        rows = cur.fetchall()

    statscur = statsconn.cursor()
    statscur.execute("UPDATE stats SET offset_preguntes = ? WHERE id_user=?",(offset_preguntes, user_id,))
    statsconn.commit()

    if len(rows) > 0:
        for row in rows:
    		statscur.execute("UPDATE stats SET ultima_pregunta_id = ? WHERE id_user=?",(row['id'], user_id,))
    		statsconn.commit()
                for ext in [ 'jpg', 'png' ]:
                    if os.path.isfile('./preguntes/'+str(row['id'])+'.'+ext):
                        #bot.send_photo(chat_id=chat_id, photo=open('tests/test.png', 'rb'))
                        bot.send_photo(chat_id=update.message.chat_id, photo=open('./preguntes/'+str(row['id'])+'.'+ext, 'rb'))

                keyboard = [[InlineKeyboardButton(row['resposta_a'], callback_data='p-'+str(row['id'])+'-a')],
                            [InlineKeyboardButton(row['resposta_b'], callback_data='p-'+str(row['id'])+'-b')],
                            [InlineKeyboardButton(row['resposta_c'], callback_data='p-'+str(row['id'])+'-c')],
                            [InlineKeyboardButton(row['resposta_d'], callback_data='p-'+str(row['id'])+'-d')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text(row['pregunta'], reply_markup=reply_markup)
    else:
        update.message.reply_text(emojize("el criteri de busqueda no troba cap resultat", use_aliases=True))

    statsconn.close()
    conn.close()


def preguntahandler(bot, update):
    query = update.callback_query
    user_id = query.from_user.id
    display_name = query.from_user.first_name

    input_data=[]
    input_data=query.data.split('-')

    if len(input_data) != 3:
      logging.debug('error input data')
      return

    tipus_input=input_data[0]
    id_referencia=input_data[1]
    resultat_referencia=input_data[2]

    # print query
    logging.debug(query)

    statsdb = config.get('bot', 'statsfile')
    statsconn = create_connection(statsdb)
    statsconn.row_factory = sqlite3.Row
    statscur = statsconn.cursor()
    statscur.execute("SELECT id,id_user,ok,failed,display_name,ultima_pregunta_id FROM stats WHERE id_user=? LIMIT 1", (user_id,))

    users = statscur.fetchall()

    # si no existeix, crear a 0
    if len(users) == 0:
      statscur = statsconn.cursor()
      statscur.execute("INSERT INTO stats(id_user,ok,failed,display_name) VALUES (?,0,0,?)",(user_id,display_name,))
      statsconn.commit()
      statscur = statsconn.cursor()
      statscur.execute("SELECT id,id_user,ok,failed,display_name FROM stats WHERE id_user=? LIMIT 1", (user_id,))
      users = statscur.fetchall()

    user=users[0]
    stats_display_name = user['display_name']

    database = config.get('bot', 'dbfile')
    conn = create_connection(database)
    # TODO: habilitar diccionari
    #conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id,pregunta,resposta_a,resposta_b,resposta_c,resposta_d,resposta_correcte FROM preguntes WHERE id=? LIMIT 1", (id_referencia,))

    rows = cur.fetchall()

    logging.debug('preguntes coincidents: '+str(len(rows)))

    for row in rows:
        response=row[1]+"\n\n"
        id_pregunta=row[0]
    	encertada=True
        # TODO: rescriure amb diccionari i canviant el callback_data a la pregunta en si
    	for i in range(2,6):
    		if len(row[i]) > 0:
    			lletra=chr(ord('a') + i-2)
    			if lletra == row[6]:
    				response+=lletra+") "+row[i]+"  :white_check_mark:\n"
    			else:
    				if lletra == resultat_referencia:
    					response+=lletra+") "+row[i]+" :x:\n"
    					encertada=False
    				else:
    					response+=lletra+") "+row[i]+"\n"

    	statscur = statsconn.cursor()

    	if encertada:
    		statscur.execute("UPDATE stats SET ok = ok + 1 WHERE id_user=?",(user_id,))
    	else:
    		statscur.execute("UPDATE stats SET failed = failed + 1 WHERE id_user=?",(user_id,))

        if (stats_display_name is None or stats_display_name!=display_name):
    	       statscur.execute("UPDATE stats SET display_name = ? WHERE id_user=?",(display_name, user_id,))
    	statsconn.commit()

        statscur = statsconn.cursor()
        statscur.execute("SELECT id_pregunta,ok,failed FROM stats_preguntes WHERE id_pregunta=? LIMIT 1", (id_pregunta,))
        preguntes = statscur.fetchall()

        if len(preguntes) > 0:
            if encertada:
                statscur.execute("UPDATE stats_preguntes SET ok = ok + 1 WHERE id_pregunta=?",(id_pregunta,))
            else:
                statscur.execute("UPDATE stats_preguntes SET failed = failed + 1 WHERE id_pregunta=?",(id_pregunta,))
        else:
            if encertada:
                statscur.execute("INSERT INTO stats_preguntes(id_pregunta,ok,failed) VALUES (?,1,0)",(id_pregunta,))
            else:
                statscur.execute("INSERT INTO stats_preguntes(id_pregunta,ok,failed) VALUES (?,0,1)",(id_pregunta,))
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


# conv_handler = ConversationHandler(
#     entry_points={
#         [CommandHandler('start', start)]
#         },
#     states={
#         PREGUNTA: [CallbackQueryHandler(first)],
#         SET_TEMA: [CallbackQueryHandler(second)]
#     },
#     fallbacks=[CommandHandler('start', start)]
# )

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('pregunta', pregunta))
updater.dispatcher.add_handler(CommandHandler('stats', stats))
updater.dispatcher.add_handler(CommandHandler('resetstats', resetstats))
updater.dispatcher.add_handler(CommandHandler('ranking', ranking))
updater.dispatcher.add_handler(CommandHandler('showversion', showversion))
updater.dispatcher.add_handler(CommandHandler('settema', setTema))
updater.dispatcher.add_handler(CommandHandler('setmodalitat', setModalitat))
updater.dispatcher.add_handler(CommandHandler('setexamen', setExamen))
updater.dispatcher.add_handler(CommandHandler('kill', showpenis))
updater.dispatcher.add_handler(CommandHandler('pegunta', showpenis))
updater.dispatcher.add_handler(CallbackQueryHandler(preguntahandler))

updater.start_polling()

updater.idle()
