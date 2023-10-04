from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn 

app = FastAPI() 

origins = ['google.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

@app.get("/")
def get_test():
    return {'hello': 'testApp.py'}
