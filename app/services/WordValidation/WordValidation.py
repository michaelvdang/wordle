from fastapi import FastAPI, Depends, status
import sqlite3
import contextlib
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    word_list_db_path: str = './var/WordList.db'

def get_word_list_db():
    with contextlib.closing(sqlite3.connect(settings.word_list_db_path)) as word_list_db:
        yield word_list_db

settings = Settings()
app = FastAPI()

@app.get('/', status_code=status.HTTP_200_OK)
def hello():
    return {'message': 'WordValidation.py'}

@app.get("/word/is-valid/{word}", status_code=status.HTTP_200_OK)
def is_valid(word: str, db: sqlite3.Connection = Depends(get_word_list_db)):
    '''
    Return true if word is in the ValidWords table, false otherwise
    '''
    if db.execute("SELECT 1 FROM ValidWords WHERE word = (?)",[word]).fetchone():
        return {'is_valid_word': True}
    else:
        return {'is_valid_word': False}

@app.post("/word/{word}", status_code=status.HTTP_201_CREATED)
def add_word(word: str, db: sqlite3.Connection = Depends(get_word_list_db)):
    '''
    Add new word to ValidWords table
    '''
    if db.execute("SELECT 1 FROM ValidWords WHERE word = (?)",[word]).fetchone():
        return {"Word already available":word}
    else:
        db.execute("INSERT INTO ValidWords (word) VALUES (?)",[word])
        return {"Word added" : word}

@app.delete("/word/{word}", status_code=status.HTTP_200_OK)
def delete_word(word: str, db: sqlite3.Connection = Depends(get_word_list_db)):
    '''
    Remove word from ValidWords table
    '''
    if db.execute("SELECT 1 FROM ValidWords WHERE word = (?)",[word]).fetchone():
         db.execute("DELETE FROM ValidWords WHERE word = (?)",[word])
         return {"Word removed" : word}
    else:
        return {"Word not found" : word}