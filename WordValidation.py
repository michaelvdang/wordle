from fastapi import FastAPI, Response
import sqlite3
app = FastAPI()

@app.get('/')
def test():
    return {'message': 'WordValidation.py'}

@app.get("/word/is-valid/{word}")
def isValid(word: str):
    connection = sqlite3.connect("./var/WordList.db",timeout=10)
    cursor = connection.cursor()
    if cursor.execute("SELECT 1 FROM ValidWords WHERE word = (?)",[word]).fetchone():
        return {'is_valid_word': True}
        return {"Word found":word}
    else:
        return {'is_valid_word': False}
        return {"Word not found" : word}

@app.post("/word/{word}")
def addword(word: str):
    connection = sqlite3.connect("./var/WordList.db", timeout=10)
    cursor = connection.cursor()
    if cursor.execute("SELECT 1 FROM ValidWords WHERE word = (?)",[word]).fetchone():
        return {"Word already available":word}
    else:
        cursor.execute("INSERT INTO ValidWords (word) VALUES (?)",[word])
        connection.commit()
        connection.close()
        return {"Word added" : word}

@app.delete("/word/{word}")
def deleteword(word: str):
    connection = sqlite3.connect("./var/WordList.db",timeout=10)
    cursor = connection.cursor()
    if cursor.execute("SELECT 1 FROM ValidWords WHERE word = (?)",[word]).fetchone():
         cursor.execute("DELETE FROM ValidWords WHERE word = (?)",[word])
         connection.commit()
         return {"Word removed" : word}
    else:
        connection.commit()
        return {"Word not found" : word}