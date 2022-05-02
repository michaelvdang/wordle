import redis

r = redis.Redis()

user_id = 1
game_id = 1
guess = 'world'
key = f"{user_id}:{game_id}"
game = {}
with r.pipeline() as pipe:
  try:
    pipe.watch(key)
    guesses_remain = int(r.lindex(key, 0))
    game['guesses_remain'] = guesses_remain
    for i in range(1, guesses_remain + 1):
      game['guesses' + str(i)] = r.lindex(key, i)
    print(game)

  except redis.WatchError:
    print("ERROR: someone tried playing this game at the same time")
