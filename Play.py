# service which stores game state in Redis
# create, update and retrieve games from users

# from logging.handlers import WatchedFileHandler
from fastapi import FastAPI, Depends
import random
import redis

def get_db():
  yield redis.Redis(host='redis', port=6379, decode_responses=True)

app = FastAPI()

@app.get('/')
def get_test():
  return {'message': 'Play.py'}

# create a new game object with 6 remaining guesses in Redis
@app.post('/play')
def play_new_game(guid: str, game_id: int, r: redis.Redis = Depends(get_db)):
  key = f"{guid}:{game_id}"
  print('new key: ', key)
  with r.pipeline() as pipe:
    try:
      pipe.watch(key)
      # TODO: raise proper error
      if r.exists(key):
        return {'status': 'error', 'message':"ERROR: this game already exists"}
      r.hset(key, 'remain', 6)
      # r.rpush(key, 6)
      pipe.unwatch()
      return {**(r.hgetall(key)), 'status': 'success'}
      # return {'game': r.lrange(key, 0, -1), 'status': 'success'}
    except redis.WatchError:
      return {'status': 'error', 'message': "RedisWatchError"}
  
# add new guess to current game
@app.put('/play')
def update_game_with_guess(guid: str, game_id: int, guess: str, r: redis.Redis = Depends(get_db)):
  key = f"{guid}:{game_id}"

  with r.pipeline() as pipe:
    try: 
      pipe.watch(key)
      remain: int = int(r.hget(key, 'remain'))
      # guesses_remain: int = int(r.lindex(key, 0))
      if remain > 0:
        pipe.multi()
        pipe.hincrby(key, 'remain', -1)
        pipe.hset(key, 'guess' + str(6 - remain + 1), guess)
        # pipe.lset(key, 0, guesses_remain - 1)
        # pipe.rpush(key, guess)
        pipe.execute()
        return {**(r.hgetall(key)), 'status': 'success'}
        # return {'game' : r.lrange(key, 0, -1), 'status': 'success'}
        # return "Updated game successfully"
      else:
        pipe.unwatch()
        return {'game' : {}, 'status': 'error', 'message': 'guesses limit reached'}
        # return "ERROR: guesses limit reached"
    except redis.WatchError:
      return {'game' : {}, 'status': 'error', 'message': 'someone tried guessing at the same time'}
      # return "ERROR: someone tried guessing at the same time"

@app.get('/play')
def restore_game(guid: str, game_id: int, r: redis.Redis = Depends(get_db)):
  key = f"{guid}:{game_id}"
  # response = {}

  with r.pipeline() as pipe:
    try:
      pipe.watch(key)
      response = r.hgetall(key)
      response['status'] = 'success'
      pipe.unwatch()
      return response
    except redis.WatchError:
      return {'status': 'error', 'message': "ERROR: someone tried playing this game at the same time"}
    except TypeError as e:
      return {'status': 'error', 'message': 'TypeError: ' + str(e)}
    except Exception as e:
      return {'status': 'error', 'message': str(e)}
