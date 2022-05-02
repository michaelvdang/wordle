import random
import redis

r = redis.Redis()

random.seed(444)
hats = {f"hat:{random.getrandbits(32)}": i for i in (
    {
        "color": "black",
        "price": 49.99,
        "style": "fitted",
        "quantity": 1000,
        "npurchased": 0,
    },
    {
        "color": "maroon",
        "price": 59.99,
        "style": "hipster",
        "quantity": 500,
        "npurchased": 0,
    },
    {
        "color": "green",
        "price": 99.99,
        "style": "baseball",
        "quantity": 200,
        "npurchased": 0,
    })
}

print(hats)

with r.pipeline() as pipe:
  for h_id, hat in hats.items():
    pipe.hmset(h_id, hat)
  pipe.execute()

r.bgsave()

print(r.hgetall("hat:56854717"))
print(r.keys())
