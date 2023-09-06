# service which stores game state in Redis
# create, update and retrieve games from users

# from logging.handlers import WatchedFileHandler
from fastapi import FastAPI, Depends
import random
import redis

def get_db():
  yield redis.Redis()

app = FastAPI()

@app.get('/')
def get_test():
  return {'message': 'Play.py'}

@app.post('/play')
def play_new_game(guid: str, game_id: int, r: redis.Redis = Depends(get_db)):
  key = f"{guid}:{game_id}"
  with r.pipeline() as pipe:
    try:
      pipe.watch(key)
      # TODO: raise proper error
      if r.exists(key):
        return {'status': 'error', 'message':"ERROR: this game already exists"}
      r.rpush(key, 6)
      pipe.unwatch()
      return {'game': r.lrange(key, 0, -1), 'status': 'success'}
    except redis.WatchError:
      return {'status': 'error', 'message': "ERROR: someone has just started the same game on this account?"}
  
@app.put('/play')
def update_game(guid: str, game_id: int, guess: str, r: redis.Redis = Depends(get_db)):
  key = f"{guid}:{game_id}"

  with r.pipeline() as pipe:
    try: 
      pipe.watch(key)
      guesses_remain: int = int(r.hget(key, 'guesses_remain'))
      # guesses_remain: int = int(r.lindex(key, 0))
      if guesses_remain > 0:
        pipe.multi()
        pipe.hset(key, 'guesses_remain', guesses_remain - 1)
        pipe.hset(key, 'guess' + 6 - guesses_remain + 1, guess)
        # pipe.lset(key, 0, guesses_remain - 1)
        # pipe.rpush(key, guess)
        pipe.execute()
        return {'game' : r.lrange(key, 0, -1), 'status': 'success'}
        # return "Updated game successfully"
      else:
        pipe.unwatch(key)
        return {'game' : {}, 'status': 'error', 'message': 'guesses limit reached'}
        # return "ERROR: guesses limit reached"
    except redis.WatchError:
      return {'game' : {}, 'status': 'error', 'message':ss 'someone tried guessing at the same time'}
      # return "ERROR: someone tried guessing at the same time"

@app.get('/play')
def restore_game(guid: str, game_id: int, r: redis.Redis = Depends(get_db)):
  key = f"{guid}:{game_id}"
  game = {}

  with r.pipeline() as pipe:
    try:
      pipe.watch(key)
      guesses_remain = int(r.hget(key, 'guesses_remain'))
      # guesses_remain = int(r.lindex(key, 0))
      game['guesses_remain'] = guesses_remain
      for i in range(1, 7):
        game['guesses' + str(i)] = r.lindex(key, i)
      game['status'] = 'success'
      return game
    except redis.WatchError:
      return {'status': 'error', 'message': "ERROR: someone tried playing this game at the same time"}
