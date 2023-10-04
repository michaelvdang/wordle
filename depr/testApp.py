from fastapi import FastAPI, Body, Depends
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

origins = ['http://localhost:3000', 'http://localhost:5173']
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=['*'], 
    allow_headers=['*']
)

class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        return response

app.add_middleware(MyMiddleware)

@app.get("/")
def get_data():
    return {'hello': 'testApp.py'}