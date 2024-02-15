from fastapi.testclient import TestClient

from WordCheck import app

client = TestClient(app)

def test_hello():
  response = client.get('/')
  assert response.status_code == 200
  assert response.json() == {'hello': 'WordCheck.py'}

def test_check_answer():
  response = client.post(
    '/answers/check',
    json={
      "game_id": 100,
      "word_id": 50,
      "guess": "vivid"
    },
  )
  assert response.status_code == 200
  result = response.json()
  print(result)
  result['absent_letters'].sort() # = result['absent_letters'].sort()
  print(result)
  assert result == {
    "absent_letters": sorted(["i", "v"]),
    "results": [0, 0, 0, 0, 2],
    "present_letters": ["d"],
  } 

def test_change_answer():
  word_id = 85
  new_word = 'older'
  response = client.put(
    '/answers/change?word_id=' + str(word_id) + '&new_word=' + new_word,
  )
  assert response.status_code == 200
  assert response.json() == {
    'status': 'success', 
    'message': f'new word for id ' + str(word_id) + ' is ' + new_word
    }

def test_get_answers_count():
  response = client.get('/answers/count')
  assert response.status_code == 200
  assert response.json() == {'count': 2309}

def test_get_correct_answer():
  game_id = 300
  response = client.get('/answers/'+ str(game_id))
  assert response.status_code == 200
  assert response.json() == {
    "word": "tiger",
    "status": "success"
  }