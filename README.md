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

