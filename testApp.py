from fastapi import FastAPI, Body, Depends

app = FastAPI()

@app.get("/")
def get_test():
    return {'hello': 'testApp.py'}