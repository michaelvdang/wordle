# stores top ten wins and streaks of each shard in Redis

# from fastapi import FastAPI, Depends
import contextlib
import sqlite3
import redis
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
REDISCLI_AUTH_PASSWORD = os.environ.get('REDISCLI_AUTH_PASSWORD')

from pathlib import Path
def is_docker():
  cgroup = Path('/proc/self/cgroup')
  return Path('/.dockerenv').is_file() or cgroup.is_file() and 'docker' in cgroup.read_text()
#('Running in Docker? ', is_docker())
if is_docker():
  host = 'redis'
else:
  host = 'localhost'
r = redis.Redis(host=host, port=6379, decode_responses=True, password=REDISCLI_AUTH_PASSWORD) # if running outside containers (like on the server)
  
# for when running services in docker in ubuntu with shared volume and
#     and setting crontab manually in terminal
path = Path('./var/')   #('Running in Windows and Docker on Windows')
if (os.name == 'posix' and os.path.exists('/var/snap')): # Docker on Windows doesn't have /var/snap
  #('Running in Docker-Ubuntu')
  path = '/var/snap/docker/common/var-lib-docker/volumes/wordle_db/_data/'

GAME1_DB = os.path.join(path, 'game1.db')
GAME2_DB = os.path.join(path, 'game2.db')
GAME3_DB = os.path.join(path, 'game3.db')

with contextlib.closing(sqlite3.connect(GAME1_DB)) as g1:
  with contextlib.closing(sqlite3.connect(GAME2_DB)) as g2:
    with contextlib.closing(sqlite3.connect(GAME3_DB)) as g3:
      games = (g1, g2, g3)
      for g in games:
        streaks = g.execute("SELECT * FROM streaks ORDER BY streak DESC LIMIT 10").fetchall()
        print('STREAKS: ', streaks)
        with r.pipeline() as pipe:
          for s in streaks:
            pipe.zadd('top_streaks', {s[0]: s[5]})
            # print(s[0], s[1])
          pipe.expire('top_streaks', 24*60*60)
          pipe.execute()
      
      for g in games: 
        wins = g.execute('SELECT * FROM wins LIMIT 10').fetchall()
        print('WINS: ', wins)
        with r.pipeline() as pipe:
          for w in wins:
            pipe.zadd('top_wins', {w[0] : w[1]})
          pipe.expire('top_wins', 24*60*60)
          pipe.execute()

print('Updated top 10 streaks and wins in Redis at ' + str(datetime.now()))

# print(r.zrevrange('top_wins', 0, 9, withscores=True))