from fastapi.testclient import TestClient
from Orchestrator import app
import os
from dotenv import load_dotenv

load_dotenv()
VITE_SECRET = os.environ.get('VITE_SECRET')

client = TestClient(app)

def test_hello():
  response = client.get('/')
  assert response.status_code == 200
  assert response.json() == {"message":"Orchestrator.py","VITE_SECRET":VITE_SECRET}