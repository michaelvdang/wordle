# service which stores game state in Redis
# create, update and retrieve games from users

# from logging.handlers import WatchedFileHandler
from fastapi import FastAPI, Depends
import random
import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDISCLI_AUTH_PASSWORD = os.environ.get('REDISCLI_AUTH_PASSWORD')
SERVER_IP = os.environ.get('SERVER_IP')
def get_redis():
  yield redis.Redis(
    host='localhost', ## DEBUGGING: use this host and run: uvicorn app.services.Play.Play:app --port 9300 --reload 
    # host='redis', 
    port=6379, 
    decode_responses=True, 
    password=REDISCLI_AUTH_PASSWORD
  )

app = FastAPI()

@app.get('/')
def get_test(r: redis.Redis = Depends(get_redis)):
  return {'message': 'Play.py',
          'SERVER_IP': SERVER_IP}

# create a new game object with 6 remaining guesses in Redis
@app.post('/play')
def play_new_game(guid: str, game_id: int, r: redis.Redis = Depends(get_redis)):
  key = f"{guid}:{game_id}"
  with r.pipeline() as pipe:
    try:
      pipe.watch(key)
      # TODO: raise proper error
      if r.exists(key):
        return {'status': 'error', 'message':"ERROR: this game already exists"}
      r.hset(key, mapping={
        'remain': 6,
        # 'present_letters': '',
        # 'absent_letters': '',
        # 'game_progress': '', # *ng** for n and g in correct position
        # 'completed': int(False),
        # 'won': int(False),
      })
      # r.hset(key, 'remain', 6)
      r.expire(key, 60*60*24) # expire in 24 hours
      # r.rpush(key, 6)
      pipe.unwatch()
      return {**(r.hgetall(key)), 'status': 'success'}
      # return {'game': r.lrange(key, 0, -1), 'status': 'success'}
    except redis.WatchError:
      return {'status': 'error', 'message': "RedisWatchError"}
  
# add new guess to current game
@app.put('/play')
def update_game_with_guess(guid: str, 
                           game_id: int, 
                           guess: str, 
                           r: redis.Redis = Depends(get_redis)):
  key = f"{guid}:{game_id}"
  with r.pipeline() as pipe:
    try: 
      remain: int = int(r.hget(key, 'remain')) # error checking, if key doesn't exist, int(NoneType) will return error
      pipe.watch(key)
      if remain > 0:
        pipe.multi()
        pipe.hincrby(key, 'remain', -1)
        pipe.hset(key, 'guess' + str(6 - remain + 1), guess)
        pipe.execute()
        return {**(r.hgetall(key)), 'status': 'success'}
      else:
        pipe.unwatch()
        return {'game' : {}, 'status': 'error', 'message': 'guesses limit reached'}
        # return "ERROR: guesses limit reached"
    except redis.WatchError:
      return {'game' : {}, 'status': 'error', 'message': 'someone tried guessing at the same time'}
      # return "ERROR: someone tried guessing at the same time"

@app.get('/play')
def restore_game(guid: str, 
                 game_id: int, 
                 r: redis.Redis = Depends(get_redis)):
  key = f"{guid}:{game_id}"

  ## do we need pipe here?
  with r.pipeline() as pipe:
    try:
      pipe.watch(key)
      response = r.hgetall(key)
      if ('remain' not in response):
        response['status'] = 'error'
        response['message'] = 'This game does not exists in Redis'
      else:
        response['status'] = 'success'
      pipe.unwatch()
      return response
    except redis.WatchError:
      return {'status': 'error', 'message': "ERROR: someone tried playing this game at the same time"}
    except TypeError as e:
      return {'status': 'error', 'message': 'TypeError: ' + str(e)}

