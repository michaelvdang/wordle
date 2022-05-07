# stores top ten wins and streaks of each shard in Redis

from fastapi import FastAPI, Depends
import contextlib
import sqlite3
import redis
import os
from datetime import datetime

r = redis.Redis()

GAME1_DB = os.path.join(os.path.dirname(__file__),'./../var/game1.db')
GAME2_DB = os.path.join(os.path.dirname(__file__),'./../var/game2.db')
GAME3_DB = os.path.join(os.path.dirname(__file__),'./../var/game3.db')
print(datetime.now())

with contextlib.closing(sqlite3.connect(GAME1_DB)) as g1:
  with contextlib.closing(sqlite3.connect(GAME2_DB)) as g2:
    with contextlib.closing(sqlite3.connect(GAME3_DB)) as g3:
      games = (g1, g2, g3)
      for g in games:
        streaks = g.execute("SELECT * FROM streaks ORDER BY streak DESC LIMIT 10").fetchall()
        with r.pipeline() as pipe:
          for s in streaks:
            pipe.zadd('top_streaks', {s[0]: s[1]})
            # print(s[0], s[1])
          pipe.execute()
      
      for g in games: 
        wins = g.execute('SELECT * FROM wins LIMIT 10').fetchall()
        with r.pipeline() as pipe:
          for w in wins:
            pipe.zadd('top_wins', {w[0] : w[1]})
          pipe.execute()


