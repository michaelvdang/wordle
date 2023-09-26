from fastapi import FastAPI, Body, Depends
from pydantic_settings import BaseSettings
from redis import asyncio as aioredis
class Config(BaseSettings):
    # The default URL expects the app to run using Docker and docker-compose.
    # redis_url: str = 'redis://localhost:16379'
    redis_url: str = 'redis://redis:6379'
config = Config()

app = FastAPI()

@app.get("/")
def get_test():
    return {'hello': 'testApp.py'}
