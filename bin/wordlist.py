#!/usr/bin/env python3

import contextlib
import sqlite3

DATABASE = './var/WordList.db'
WORDLIST_SCRIPT = './share/WordList.sql'

with contextlib.closing(sqlite3.connect(DATABASE)) as db:
  db.execute("DROP TABLE IF EXISTS ValidWords;")
  with open(WORDLIST_SCRIPT) as f:
    db.executescript(f.read())
    db.commit()
    sql = "SELECT * FROM ValidWords LIMIT 10;"
    print(db.execute(sql).fetchall())