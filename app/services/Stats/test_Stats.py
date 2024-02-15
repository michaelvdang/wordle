from fastapi.testclient import TestClient
from Stats import app
import os
from dotenv import load_dotenv

load_dotenv()
VITE_SECRET = os.environ.get('VITE_SECRET')

client = TestClient(app)

def test_hello():
  response = client.get('/')
  assert response.status_code == 200
  assert response.json() == {
    "message": "hello world",
    "message2": "UserStatsRedis.py",
    "VITE_SECRET": VITE_SECRET
  }