# service which stores game state in Redis
# create, update and retrieve games from users

# from logging.handlers import WatchedFileHandler
from fastapi import FastAPI, Depends, status
import random
import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDISCLI_AUTH_PASSWORD = os.environ.get('REDISCLI_AUTH_PASSWORD')
VITE_SECRET = os.environ.get('VITE_SECRET')
def get_redis():
  yield redis.Redis(
    # host='localhost', ## DEBUGGING: use this host and run: uvicorn app.services.Play.Play:app --port 9300 --reload 
    host='redis', 
    port=6379, 
    decode_responses=True, 
    password=REDISCLI_AUTH_PASSWORD
  )

app = FastAPI()

@app.get('/', status_code=status.HTTP_200_OK)
def hello(r: redis.Redis = Depends(get_redis)):
  return {'message': 'Play.py',
          # 'VITE_SERVER_IP': VITE_SERVER_IP,
          'VITE_SECRET': VITE_SECRET,
          }

# create a new game object with 6 remaining guesses in Redis
@app.post('/play', status_code=status.HTTP_201_CREATED)
def play_new_game(guid: str, game_id: int, r: redis.Redis = Depends(get_redis)):
  '''
  Create a new key in Redis that is of the form: <guid>:<game_id>
  with value 'remain' '6'
  Return the newly created object along with a 'status' key
  '''
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
      # game = {
      #   'remain': 6,
      #   # 'present_letters': '',
      #   # 'absent_letters': '',
      #   # 'game_progress': '', # *ng** for n and g in correct position
      #   # 'completed': int(False),
      #   # 'won': int(False),
      # }
      # r.hset(key, mapping=game)
      r.expire(key, 60*60*24) # expire in 24 hours
      pipe.unwatch()
      return {**(r.hgetall(key)), 'status': 'success'}
    except redis.WatchError:
      return {'status': 'error', 'message': "RedisWatchError"}
  
# add new guess to current game
@app.put('/play', status_code=status.HTTP_201_CREATED)
def update_game_with_guess(guid: str, 
                           game_id: int, 
                           guess: str, 
                           r: redis.Redis = Depends(get_redis)):
  '''
  Add a guess to game stored on Redis with key <guid>:<game_id>
  The key for this guess is one plus the highest guess# stored in Redis
  Return the game object and status on success
    or an empty game object and status if not found or an excpetion occurred
  '''
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
    except redis.WatchError:
      return {'game' : {}, 'status': 'error', 'message': 'someone tried guessing at the same time'}

@app.get('/play', status_code=status.HTTP_200_OK)
def restore_game(guid: str, 
                 game_id: int, 
                 r: redis.Redis = Depends(get_redis)):
  '''
  Return a game from Redis that matches the key <guid>:<game_id>
    or a JSON with status and message on failure or exception
  '''
  key = f"{guid}:{game_id}"

  with r.pipeline() as pipe:
    try:
      pipe.watch(key)
      response = r.hgetall(key)
      if ('remain' not in response):
        response['status'] = 'error'
        response['remain'] = 0
        response['message'] = 'This game does not exists in Redis'
      else:
        response['status'] = 'success'
      pipe.unwatch()
      return response
    except redis.WatchError:
      return {'status': 'error', 'message': "ERROR: someone tried playing this game at the same time"}
    except TypeError as e:
      return {'status': 'error', 'message': 'TypeError: ' + str(e)}

