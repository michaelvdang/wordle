import logging
import sqlite3
import contextlib

from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel, BaseSettings


class Settings(BaseSettings):
    answers_database: str = './var/Answers.db'

    class Config:
        env_file = ".envWordCheck"


class Game(BaseModel):
    game_id: int
    word_id: int
    guess: str


def get_db():
    with contextlib.closing(sqlite3.connect(settings.answers_database)) as db:
        yield db


def get_logger():
    return logging.getLogger(__name__)


settings = Settings()
app = FastAPI()


@app.post("/answers/check")
def checkAnswer(game: Game, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute(
        "SELECT * FROM Answers WHERE word_id = ? LIMIT 1", [game.word_id]).fetchone()
    #return row[1]
    answer = row[1]
    guess = game.guess
    results = []
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            results.append('G')
        elif guess[i] in answer:
            results.append('Y')
        else:
            results.append('N')
    return results


@app.put("/answers/change")
def changeAnswer(word_id: int, new_word: str, db: sqlite3.Connection = Depends(get_db)):
    db.execute("UPDATE Answers SET gameword = (?) WHERE word_id = ? LIMIT 1", [
               new_word, word_id]).fetchone()
    db.commit()
    row = db.execute(
        "SELECT * FROM Answers WHERE word_id = ? LIMIT 1", [word_id]).fetchone()
    return f'new word for id {word_id} is {row[1]}'
