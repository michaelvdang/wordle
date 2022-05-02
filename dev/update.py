import redis

r = redis.Redis()

user_id = 1
game_id = 1
guess = 'world'
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
  except redis.WatchError:
    print("ERROR: someone tried guessing at the same time")
