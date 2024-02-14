import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDISCLI_AUTH_PASSWORD = os.environ.get('REDISCLI_AUTH_PASSWORD')
def get_redis():
  yield redis.Redis(
    # host='localhost', 
    host='redis', 
    port=6379, 
    decode_responses=True, 
    password=REDISCLI_AUTH_PASSWORD
  )

key = f"d6ff7451-147f-3657-831a-246df9f7b166:2017"

def f():
  # r = get_redis()
  r = redis.Redis(
    host='localhost', 
    # host='redis', 
    port=6379, 
    decode_responses=True, 
    password=REDISCLI_AUTH_PASSWORD
  )
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

print(f())