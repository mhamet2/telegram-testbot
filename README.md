# telegram-testbot

## config failed

testbot.config:

* token: bot token as provided by BotFather
* dbfile: sqlite db with th questions and answers
* statsfile: sqlite db to store rankings
* teoriafile: sqlite db with lessons
* admins: not used (comma separated)
* trolls: list of trolls (comma separated)

example file:

```
[bot]

token = ...
dbfile = questionsdb.sqlite
statsfile = statsdb.sqlite
teoriafile = teoria.sqlite
admins = ...
trolls = ...
```

## statsfile

```
CREATE TABLE `stats` (
	`id`	INTEGER,
	`id_user`	NUMERIC NOT NULL UNIQUE,
	`ok`	NUMERIC DEFAULT 0,
	`failed`	NUMERIC DEFAULT 0,
	`display_name`	TEXT DEFAULT '',
	`offset_preguntes`	INTEGER NOT NULL DEFAULT 0,
	`tema`	TEXT NOT NULL DEFAULT '',
	`examen`	TEXT NOT NULL DEFAULT '',
	`modalitat`	TEXT NOT NULL DEFAULT 'PER',
	`ultima_pregunta_id`	INTEGER,
	PRIMARY KEY(id)
);
```

## dbfile

```
CREATE TABLE `preguntes` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`pregunta`	TEXT,
	`resposta_a`	TEXT,
	`resposta_b`	TEXT,
	`resposta_c`	TEXT,
	`resposta_d`	TEXT,
	`resposta_correcte`	TEXT,
	`tema`	TEXT,
	`examen`	TEXT,
	`modalitat`	TEXT
);
```

## teoriafile

```
CREATE TABLE `temari` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`nom`	TEXT UNIQUE,
	`dades`	TEXT,
	`ordre`	INTEGER DEFAULT 9999
);
```
