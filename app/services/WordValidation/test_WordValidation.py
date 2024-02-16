from fastapi.testclient import TestClient

from WordValidation import app

c = TestClient(app)

def test_hello():
  res = c.get('/')
  assert res.status_code == 200
  assert res.json() == {'message': 'WordValidation.py', 'deploy': 'no deploy'}

def test_is_valid():
  word = 'grunt'
  res = c.get('/word/is-valid/' + word)
  assert res.status_code == 200
  assert res.json() == {
    "is_valid_word": True
  }
  
  word = 'gurnt'
  res = c.get('/word/is-valid/' + word)
  assert res.status_code == 200
  assert res.json() == {
    "is_valid_word": False
  }
  
def test_add_word():
  word = 'potus'
  res = c.post('/word/' + word)
  assert res.status_code == 201
  assert res.json() == {
    "Word added": word
  }

def test_delete_word():
  word = 'grunt'
  res = c.delete('/word/' + word)
  assert res.status_code == 200
  assert res.json() == {"Word removed" : word}
  word = 'diamond'
  res = c.delete('/word/' + word)
  assert res.status_code == 200
  assert res.json() == {"Word not found" : word}

