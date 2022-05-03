from fastapi import FastAPI, Depends
import contextlib
import sqlite3
import redis

r = redis.Redis()

GAME1_DB = './var/game1.db'
GAME2_DB = './var/game2.db'
GAME3_DB = './var/game3.db'


with contextlib.closing(sqlite3.connect(GAME1_DB)) as g1:
  with contextlib.closing(sqlite3.connect(GAME2_DB)) as g2:
    with contextlib.closing(sqlite3.connect(GAME3_DB)) as g3:
      games = (g1, g2, g3)
      for g in games:
        streaks = g.execute("SELECT * FROM streaks ORDER BY streak DESC LIMIT 10").fetchall()
        with r.pipeline() as pipe:
          for s in streaks:
            pipe.zadd('top_streaks', {s[0]: s[1]}, nx = True)
            # print(s[0], s[1])
          pipe.execute()
      
      for g in games: 
        wins = g.execute('SELECT * FROM wins LIMIT 10').fetchall()
        with r.pipeline() as pipe:
          for w in wins:
            pipe.zadd('top_wins', {w[0] : w[1]}, nx=True)
          pipe.execute()


