# a service that stores game state in SQLite
from fastapi import FastAPI, Depends 
import contextlib
import uuid
import sqlite3
from pydantic import BaseModel, BaseSettings

USER_DB = './var/users.db'
GAME1_DB = './var/game1.db'
GAME2_DB = './var/game2.db'
GAME3_DB = './var/game3.db'
LIVEGAME_DB = './var/LiveGames.db'


class Game(BaseModel):
  user_id: int
  game_id: int
  guess1: str
  guess2: str
  guess3: str
  guess4: str
  guess5: str


class Settings(BaseSettings):
  user_db: str = USER_DB
  game1db: str = GAME1_DB
  game2db: str = GAME2_DB
  game3db: str = GAME3_DB
  livegame_db: str = LIVEGAME_DB

  class Config():
      env_file = '.env'


def get_db():
    with contextlib.closing(sqlite3.connect(settings.user_db)) as udb:
        yield udb


def get_db1():
    with contextlib.closing(sqlite3.connect(settings.game1db)) as g1:
        yield g1


def get_db2():
    with contextlib.closing(sqlite3.connect(settings.game2db)) as g2:
        yield g2


def get_db3():
    with contextlib.closing(sqlite3.connect(settings.game3db)) as g3:
        yield g3


def get_livegamedb():
  with contextlib.closing(sqlite3.connect(settings.livegame_db)) as livegame_db:
    yield livegame_db

settings = Settings()
app = FastAPI()


@app.get("/")
def hello():
    return {"message": "hello world", "message2": "monster"}

# check that the game has valid user and user has not played this game before 


def verify_game(user_id: int, game_id: int,
                u: sqlite3.Connection = Depends(get_db),
                g1: sqlite3.Connection = Depends(get_db1),
                g2: sqlite3.Connection = Depends(get_db2),
                g3: sqlite3.Connection = Depends(get_db3)):
  # TODO: change field type for guid to actual guid type
  # cannot convert a guid str back to int
  guid = uuid.uuid4()

  (uc, gc1, gc2, gc3) = (db.cursor() for db in (u, g1, g2, g3))
  games_dbs = (gc1, gc2, gc3)
  user = uc.execute("SELECT * FROM users WHERE user_id=?",
                    [user_id]).fetchone()
  # TODO: raise HTTP error
  if not user:
    return {"404 ERROR: this user doesn't exist"}

  # TODO: guid should be user[0] if user[0] were a real guid type
  prev_game = games_dbs[int(guid) % 3].execute("SELECT * FROM games WHERE user_id=? AND game_id=?",
                                               [user_id, game_id]).fetchone()

  # TODO: raise HTTP error
  if prev_game:
    return "409 CONFLICT: this game has already been played"
  return "user exists and game has not been played before" # not in game shards

@app.post("/play")
def create_game(user_id: int, game_id: int, 
                u: sqlite3.Connection = Depends(get_db),
                g1: sqlite3.Connection = Depends(get_db1), 
                g2: sqlite3.Connection = Depends(get_db2), 
                g3: sqlite3.Connection = Depends(get_db3),
                lg: sqlite3.Connection = Depends(get_livegamedb)):

  print(verify_game(user_id, game_id, u, g1, g2, g3))
  
  lgc = lg.cursor()

  # TODO: check LiveGames for conflict? 
  # integrity checks for this already

  # create new game in LiveGames.db
  try:
    lgc.execute(
        "INSERT INTO LiveGames VALUES (?,?,6,NULL,NULL,NULL,NULL,NULL,NULL)", [user_id, game_id])
  except sqlite3.IntegrityError:
        return 'Integrity error: this game is being played'
  lg.commit()
  return 'New game created'

@app.put("/play")
def update_game(user_id: int, game_id: int, guess: str,
                u: sqlite3.Connection = Depends(get_db),
                g1: sqlite3.Connection = Depends(get_db1),
                g2: sqlite3.Connection = Depends(get_db2),
                g3: sqlite3.Connection = Depends(get_db3),
                lg: sqlite3.Connection = Depends(get_livegamedb)):
  print(verify_game(user_id, game_id, u, g1, g2, g3))
  # retrieve LiveGame
  # check if >5 guesses
  # update LiveGame
  lgc = lg.cursor()
  curr_game = lgc.execute('''SELECT * FROM LiveGames 
          WHERE user_id=? AND game_id=?''', [user_id, game_id]).fetchone()
  if not curr_game:
    return "404 ERROR: this game does not exist"
    # create_game(user_id, game_id, u, g1, g2, g3, lg)
    # curr_game = lgc.execute('''SELECT * FROM LiveGames 
    #       WHERE user_id=? AND game_id=?''', [user_id, game_id]).fetchone()
  if guess in curr_game[3:]:
    return 'ERROR: this word has been played before, try a different word'
  if curr_game[2] < 1:
    return 'ERROR: You have used all your 6 guesses'  
  guesses_remain = curr_game[2] - 1
  game_update_cmd = '''
    UPDATE LiveGames 
    SET guesses_remain=?,
        guess''' + str(6 - guesses_remain) + '=?'
  lgc.execute(game_update_cmd, [guesses_remain, guess])
  lg.commit()
  return 'Game state updated'

@app.get("/play")
def restore_game(user_id: int, game_id: int,
                 u: sqlite3.Connection = Depends(get_db),
                 g1: sqlite3.Connection = Depends(get_db1),
                 g2: sqlite3.Connection = Depends(get_db2),
                 g3: sqlite3.Connection = Depends(get_db3),
                 lg: sqlite3.Connection = Depends(get_livegamedb)):
  print(verify_game(user_id, game_id, u, g1, g2, g3))
  lgc = lg.cursor()
  curr_game = lgc.execute('''SELECT * FROM LiveGames 
          WHERE user_id=? AND game_id=?''', [user_id, game_id]).fetchone()
  if not curr_game:
    return "404 ERROR: this game does not exist"
  lg.commit()
  return curr_game
  























