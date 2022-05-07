# create, update and retrieve games from users

from logging.handlers import WatchedFileHandler
from fastapi import FastAPI, Depends
import random
import redis

def get_db():
  yield redis.Redis()

app = FastAPI()

@app.post('/play')
def play_new_game(user_id: int, game_id: int, r: redis.Redis = Depends(get_db)):
  key = f"{user_id}:{game_id}"
  with r.pipeline() as pipe:
    try:
      pipe.watch(key)
      # TODO: raise proper error
      if r.exists(key):
        return "ERROR: this game already exists"
      r.rpush(key, 6)
      pipe.unwatch()
      return "Started new game"
    except redis.WatchError:
      return "ERROR: someone has just started the same game on this account?"
  
@app.put('/play')
def update_game(user_id: int, game_id: int, guess: str, r: redis.Redis = Depends(get_db)):
  key = f"{user_id}:{game_id}"

  with r.pipeline() as pipe:
    try: 
      pipe.watch(key)
      guesses_remain: int = int(r.lindex(key, 0))
      if guesses_remain > 0:
        pipe.multi()
        pipe.lset(key, 0, guesses_remain - 1)
        pipe.rpush(key, guess)
        pipe.execute()
        return "Updated game successfully"
      else:
        return "ERROR: guesses limit reached"
    except redis.WatchError:
      return "ERROR: someone tried guessing at the same time"

@app.get('/play')
def restore_game(user_id: int, game_id: int, r: redis.Redis = Depends(get_db)):
  key = f"{user_id}:{game_id}"
  game = {}

  with r.pipeline() as pipe:
    try:
      pipe.watch(key)
      guesses_remain = int(r.lindex(key, 0))
      game['guesses_remain'] = guesses_remain
      for i in range(1, 7):
        game['guesses' + str(i)] = r.lindex(key, i)
      # for i in range()
      return game
    except redis.WatchError:
      return "ERROR: someone tried playing this game at the same time"
