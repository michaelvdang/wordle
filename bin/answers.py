#!/usr/bin/env python3

import contextlib
import sqlite3

DATABASE = './var/Answers.db'
ANSWERS_SCRIPT = './share/Answers.sql'

with contextlib.closing(sqlite3.connect(DATABASE)) as db:
  db.execute("DROP TABLE IF EXISTS Answers;")
  db.execute("DROP TABLE IF EXISTS Games;")
  db.execute("DROP VIEW IF EXISTS Game_words;")
  with open(ANSWERS_SCRIPT) as f:
    db.executescript(f.read())
    db.commit()
    sql = "SELECT * FROM Answers LIMIT 10;"
    print(db.execute(sql).fetchall())