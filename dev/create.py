import redis

r = redis.Redis()

user_id = 1
game_id = 1
guess = 'hello'
key = f"{user_id}:{game_id}"

key = f"{user_id}:{game_id}"
with r.pipeline() as pipe:
  try:
    pipe.watch(key)
    # TODO: raise proper error
    if r.exists(key):
      print("ERROR: this game already exists")
    r.rpush(key, 6)
    pipe.unwatch()
    print("Started new game")
  except redis.WatchError:
    print("ERROR: someone has just started the same game on this account?")
