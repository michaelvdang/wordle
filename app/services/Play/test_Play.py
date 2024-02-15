from fastapi.testclient import TestClient
from Play import app
import os
from dotenv import load_dotenv

load_dotenv()

VITE_SECRET = os.environ.get('VITE_SECRET')

c = TestClient(app)

def test_hello():
  res = c.get('/')
  assert res.status_code == 200
  assert res.json() == {'message': 'Play.py', 'VITE_SECRET': VITE_SECRET}

def test_play_new_game():
  guid = 'test-guid-123'
  game_id = 123
  res = c.post('/play?guid=' + guid + '&game_id=' + str(game_id))
  assert res.status_code == 201
  assert res.json() == {
    "remain": 6,
    "status": "success"
  }
    