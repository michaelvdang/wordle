from fastapi.testclient import TestClient
from Orchestrator import app
import os
from dotenv import load_dotenv

load_dotenv()
VITE_SECRET = os.environ.get('VITE_SECRET')

c = TestClient(app)

def test_hello():
  res = c.get('/')
  assert res.status_code == 200
  assert res.json() == {"message":"Orchestrator.py","VITE_SECRET":VITE_SECRET}

# for other methods, set up a test database to run test, start with WordCheck and WordValidation
  
# def test_start_new_game():
#   username = 'user1'
#   res = c.post('/game/new?username=' + username)
#   assert res.status_code == 201
#   game = res.json()
#   assert game['status'] == 'success' 
#   assert game['remain'] == 6

