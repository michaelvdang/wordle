from fastapi import FastAPI, Response
app = FastAPI()

@app.get('/')
def test():
    return {'message': 'root'}

@app.get('/static')
def static_func():
    return {'message': 'Reached static-endpoint'}

@app.get("/dynamic/{word}")
def dynamic_func(word: str):
  return {'message': 'dynamic-endpoint',
          'parameter': word}