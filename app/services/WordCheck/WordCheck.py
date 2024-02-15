import logging
import sqlite3
import contextlib

from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel#, BaseSettings
from pydantic_settings import BaseSettings
# from models import Game

class Game(BaseModel):
    game_id: int
    word_id: int
    guess: str

class Settings(BaseSettings):
    # answers_database: str = '/wordle/var/Answers.db'  # for container
    answers_database: str = './var/Answers.db'    # for non-container

    # class Config:
    #     env_file = ".envWordCheck"


def get_db():
    with contextlib.closing(sqlite3.connect(settings.answers_database)) as db:
        yield db


def get_logger():
    return logging.getLogger(__name__)


settings = Settings()
app = FastAPI()

@app.get("/")
def hello():
    return {'hello': 'WordCheck.py'}

@app.post("/answers/check")
def check_answer(game: Game, db: sqlite3.Connection = Depends(get_db)):
    '''
    Check a guess against the correct ANSWER for a give game_id
    class Game(BaseModel):
        game_id: int
        word_id: int
        guess: str
    return: a JSON object with 3 keys
        - results: a list of length 5 from [0,1,2], 0 for miss, 1 for present, 2 for exact
        - present_letters: a set of letters present in the ANSWER
        - absent_letter: a set of letters users have guessed that are not in present_letters
    '''
    row = db.execute(
        "SELECT * FROM Answers WHERE word_id = ? LIMIT 1", [game.word_id]).fetchone()
    #return row[1]
    answer = row[1]
    guess = game.guess
    results = []
    present_letters = set()
    absent_letters = set()
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            results.append(2)
            present_letters.add(guess[i])
        elif guess[i] in answer:
            results.append(1)
            present_letters.add(guess[i])
        else:
            results.append(0)
            absent_letters.add(guess[i])
    return {'results': results, 'present_letters': present_letters, 'absent_letters': absent_letters}

@app.put("/answers/change")
def change_answer(word_id: int, new_word: str, db: sqlite3.Connection = Depends(get_db)):
    '''
    Change the correct answer to new_word for a the given word_id
    Return a JSON with keys 'status' and 'message'
    '''
    db.execute("UPDATE Answers SET gameword = (?) WHERE word_id = ?", [
               new_word, word_id]).fetchone()
    db.commit()
    row = db.execute(
        "SELECT * FROM Answers WHERE word_id = ? LIMIT 1", [word_id]).fetchone()
    return {'status': 'success', 'message': f'new word for id {word_id} is {row[1]}'}

@app.get("/answers/count")
def get_answers_count(db: sqlite3.Connection = Depends(get_db)):
    '''
    Gets the number of answers in the database
    Return a JSON object with key 'count' for number of answers in database
    '''
    row = db.execute('SELECT count(*) FROM Answers').fetchone()
    return {'count': row[0]}

@app.get("/answers/{game_id}")
def get_correct_answer(game_id: int, db: sqlite3.Connection = Depends(get_db)):
    '''
    Return the correct answer for a give game_id
    '''
    row = db.execute("SELECT gameword FROM Game_words WHERE game_id = (?)", [game_id]).fetchone()
    print(row)
    return {'word': row[0], 'status': 'success'}