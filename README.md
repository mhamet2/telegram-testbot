# telegram-testbot

## config failed

testbot.config:

* token: bot token as provided by BotFather
* dbfile: sqlite db with th questions and answers
* statsfile: sqlite file to store rankings

```
[bot]

token = ...
dbfile = per.sqlite
statsfile = perstats.sqlite
```

## statsfile

```
CREATE TABLE stats
  (id INTEGER PRIMARY KEY,
    id_user NUMERIC,
    ok NUMERIC,
    failed NUMERIC)
```

## dbfile

```
CREATE TABLE preguntes
  (id INTEGER PRIMARY KEY,
    pregunta TEXT,
    resposta_a TEXT,
    resposta_b TEXT,
    resposta_c TEXT,
    resposta_d TEXT,
    resposta_correcte TEXT)
```

## sample data

```
{'from': {'first_name': u'Jordi', 'is_bot': False, 'id': 13906317, 'language_code': u'en'}, 'chat_instance': u'66867255455748788', 'message': {'delete_chat_photo': False, 'new_chat_photo': [], 'from': {'username': u'pertesterbot', 'first_name': u'PER', 'is_bot': True, 'id': 421304510}, 'text': u'\xbfCu\xe1l es el tel\xe9fono de salvamento mar\xedtimo?', 'caption_entities': [], 'entities': [], 'channel_chat_created': False, 'new_chat_members': [], 'supergroup_chat_created': False, 'chat': {'first_name': u'Jordi', 'type': u'private', 'id': 13906317}, 'photo': [], 'date': 1517647108, 'group_chat_created': False, 'message_id': 815, 'new_chat_member': None}, 'data': u'd', 'id': u'59727180429809359'}
{'from': {'first_name': u'Jordi', 'is_bot': False, 'id': 13906317, 'language_code': u'en'}, 'chat_instance': u'66867255455748788', 'message': {'delete_chat_photo': False, 'new_chat_photo': [], 'from': {'username': u'pertesterbot', 'first_name': u'PER', 'is_bot': True, 'id': 421304510}, 'text': u'\xbfQu\xe9 uso debe hacerse de los baldes contra incendios?', 'caption_entities': [], 'entities': [], 'channel_chat_created': False, 'new_chat_members': [], 'supergroup_chat_created': False, 'chat': {'first_name': u'Jordi', 'type': u'private', 'id': 13906317}, 'photo': [], 'date': 1517647286, 'group_chat_created': False, 'message_id': 817, 'new_chat_member': None}, 'data': u'c', 'id': u'59727177694688860'}
```


```
2018-02-04 16:14:37,281 - telegram.ext.dispatcher - DEBUG - Processing Update: {'message': {'delete_chat_photo': False, 'new_chat_photo': [], 'from': {'first_name': u'Jordi', 'is_bot': False, 'id': 13906317, 'language_code': u'en'}, 'text': u'/pregunta', 'caption_entities': [], 'entities': [{'length': 9, 'type': u'bot_command', 'offset': 0}], 'channel_chat_created': False, 'new_chat_members': [], 'supergroup_chat_created': False, 'chat': {'first_name': u'Jordi', 'type': u'private', 'id': 13906317}, 'photo': [], 'date': 1517760877, 'group_chat_created': False, 'message_id': 1460, 'new_chat_member': None}, 'update_id': 547626922}
```
