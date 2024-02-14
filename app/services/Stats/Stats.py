# top 30 winners and streaks are stored in Redis
# the rest are in SQLite database

from fastapi import FastAPI, Depends
import contextlib
import datetime
import sqlite3
from pydantic import BaseModel#, BaseSettings
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
import json
import uuid
import redis
import os
from dotenv import load_dotenv

load_dotenv()
# .env file is stored in the same directory as this file
REDISCLI_AUTH_PASSWORD = os.environ.get('REDISCLI_AUTH_PASSWORD')
VITE_SERVER_IP = os.environ.get('VITE_SERVER_IP')
VITE_DOMAIN_NAME = os.environ.get('VITE_DOMAIN_NAME')
VITE_SECRET = os.environ.get('VITE_SECRET')
def get_redis():
    yield redis.Redis(
                    # host='localhost',
                    host='redis', 
                    port=6379, 
                    decode_responses=True, 
                    password=REDISCLI_AUTH_PASSWORD,
                    # username=username
                    )

USER_DB = './var/users.db'
GAME1_DB = './var/game1.db'
GAME2_DB = './var/game2.db'
GAME3_DB = './var/game3.db'


class Result(BaseModel):
    guesses: int
    won: bool
    completed: bool


class Settings(BaseSettings):
    user_db: str = USER_DB
    game1db: str = GAME1_DB
    game2db: str = GAME2_DB
    game3db: str = GAME3_DB


def get_udb():
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


settings = Settings()
app = FastAPI()

origins = [     # curl and local browser are always allowed
    "http://localhost:5173",    # needs this even when React App is local and Orc is remote
    "http://" + str(VITE_SERVER_IP),
    "http://" + str(VITE_DOMAIN_NAME),
    "https://" + str(VITE_DOMAIN_NAME)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {"message": "hello world", 
            "message2": "UserStatsRedis.py",
            # "VITE_DOMAIN_NAME": "https://" + VITE_DOMAIN_NAME,
            # "VITE_SERVER_IP": VITE_SERVER_IP, 
            "VITE_SECRET": VITE_SECRET,
            }

# insert finished game into the correct shard based on guid for storage
@app.post("/stats/games/store-result", status_code=201)
def store_game_result(
        username: str, 
        user_id: int, 
        game_id: int, 
        result: Result, 
        g1: sqlite3.Connection = Depends(get_db1), 
        g2: sqlite3.Connection = Depends(get_db2), 
        g3: sqlite3.Connection = Depends(get_db3),
        r: redis.Redis = Depends(get_redis)):
    try:
        gamedb = (g1, g2, g3)
        guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id)) # NOTE: generating guid from user_id because game object pulled from stats.db don't have username in them, only user_id, and joining stats.db.games with users table would be too much of a hassle and I don't want to  redesign the DB 

        finished = datetime.date.today()
        guesses = result.guesses
        won = result.won
        gamedb[int(guid) % 3].execute(
            """
            INSERT INTO games(guid, user_id, game_id, finished, guesses, won)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            [str(guid), user_id, game_id, finished, guesses, won]
        )
        gamedb[int(guid) % 3].commit()
        r.delete(str(guid) + ':' + str(game_id))
        return {'Success' : 'Game recorded'}

    except sqlite3.IntegrityError:
        return 'Integrity error, there is another game with this game_id'

# return top 10 winners
@app.get('/stats/top-winners', status_code=200)
def get_top_winners(r: redis.Redis = Depends(get_redis)):
    top_wins = r.zrevrange('top_wins', 0, 9, withscores=True)
    
    return [(user_id, int(score)) for (user_id, score) in top_wins]

# return top 10 streaks
@app.get('/stats/top-streaks', status_code=200)
def get_top_streaks(r: redis.Redis = Depends(get_redis)):
    top_streaks = r.zrevrange('top_streaks', 0, 9, withscores=True)
    return [(user_id, int(score)) for (user_id, score) in top_streaks]

@app.get('/stats/top-streaks-and-winners', status_code=200)
def get_top_streaks_and_winners(r: redis.Redis = Depends(get_redis)):
    top_wins = r.zrevrange('top_wins', 0, 9, withscores=True)
    top_streaks = r.zrevrange('top_streaks', 0, 9, withscores=True)
    return {'top_wins': top_wins, 'top_streaks': top_streaks}

# return stats for a given user
@app.get('/stats/users', status_code=200)
def get_user_stats(
        user_id: int, 
        username: str,
        udb: sqlite3.Connection = Depends(get_udb), 
        g1: sqlite3.Connection = Depends(get_db1), 
        g2: sqlite3.Connection = Depends(get_db2), 
        g3: sqlite3.Connection = Depends(get_db3)):
    username = username.lower()
    gamedb = (g1, g2, g3)
    guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id)) # NOTE: generating guid from user_id because game object pulled from stats.db don't have username in them, only user_id, and joining stats.db.games with users table would be too much of a hassle and I don't want to  redesign the DB 
    # print('guid: ', guid)
    gc = gamedb[int(guid) % 3].cursor()
    # games = gc.execute('select * from games where user_id=?', [user_id]).fetchall()
    games = gc.execute(
        '''
        SELECT *
        FROM games WHERE user_id=? 
        ORDER BY finished;
        ''', [user_id]).fetchall()
    stats = {}
    wins_count = 0
    for game in games:
        if game[5] == 1:
            wins_count += 1
    stats['games_won'] = wins_count
    stats['games_played'] = len(games)
    if (len(games)): 
        stats['win_percentage'] = wins_count / len(games)
    else:
        stats['win_percentage'] = 0
    # print(games)
    # NOTE: this sql might not be working correctly, returnin NoneType and zeroes for current_streak and max_win_streak, avg_guesses
    res = gc.execute(
        '''
        WITH GameRows AS (
        SELECT 
            ROW_NUMBER() OVER (ORDER BY finished) as row_num, 
            g.user_id, 
            username, 
            finished, 
            won 
        FROM Games g 
        JOIN Users u ON g.user_id=u.user_id
        WHERE g.user_id=?
        ORDER BY g.user_id, row_num
        ),
        RunGroups AS (
        SELECT 
            ng1.row_num, ng1.user_id, ng1.won, ng1.finished,
            (SELECT COUNT(*)
            FROM GameRows ng2
            WHERE ng1.won <> ng2.won
            AND ng1.row_num > ng2.row_num
            AND ng1.user_id = ng2.user_id) AS RunGroup
        FROM GameRows ng1
        ), 
        Streaks AS (
            SELECT 
                row_num, 
                user_id, 
                won, 
                MIN(finished) AS beginning, 
                MAX(finished) AS ending, 
                COUNT(*) AS streak
            FROM RunGroups
            GROUP BY user_id, won, RunGroup
            ORDER BY user_id, row_num
        )
        SELECT streak, won, 
            (SELECT max(streak) FROM streaks WHERE user_id=?) AS max_streak,
            (SELECT avg(guesses) FROM games WHERE user_id=? and won=1) AS average_guesses
        FROM Streaks 
        WHERE row_num=(SELECT MAX(row_num) FROM Streaks);
        ''', [user_id, user_id, user_id]).fetchone()
    print('UserStatRedis.py res: ', res)
    if res and len(res):
        stats['current_streak'] = {'streak': res[0], 'won': res[1]}
        stats['max_win_streak'] = res[2]
        stats['average_guesses'] = res[3]
    else:
        stats['current_streak'] = {'streak': 0, 'won': 0}
        stats['max_win_streak'] = 0
        stats['average_guesses'] = 0
    return stats

@app.get('/stats/username/{user_id}')
def get_username(user_id: int, udb: sqlite3.Connection = Depends(get_udb)):
    print('user_id: ', user_id)
    print('type: ', type(user_id))  
    row = udb.execute('SELECT * FROM users WHERE user_id=?', [user_id])
    try:
        user = row.fetchone()
        return {'guid': str(user[0]), 'user_id': user[1], 'username': user[2]}
    except TypeError:
        return -1

# return user info for a given username
@app.get('/stats/id/{username}')
def get_user_id(username: str, udb: sqlite3.Connection = Depends(get_udb)):
    username = username.lower()
    print('username: ', username)
    print('type: ', type(username))
    # row = udb.execute('SELECT * FROM users WHERE username="mdang4"')
    row = udb.execute('SELECT * FROM users WHERE username=?', [username])
    try:
        user = row.fetchone()
        print('row: ', row)
        print('user: ', user)
        return {
            'guid': str(user[0]), 
            'user_id': int(user[1]), 
            'username': str(user[2])
        }
    except TypeError:
        return -1
    
# create new user
@app.post('/stats/users/new', status_code=201)
def create_user(username: str, 
        udb: sqlite3.Connection = Depends(get_udb),
        g1: sqlite3.Connection = Depends(get_db1), 
        g2: sqlite3.Connection = Depends(get_db2), 
        g3: sqlite3.Connection = Depends(get_db3)):
    username = username.lower()
    try:
        # check that username is unique
        row = udb.execute('SELECT * FROM users WHERE username=?', [username])
        existing_user = row.fetchone()
        if existing_user:
            print('ERROR existing user: ', existing_user)                           # Debugging
            return {'Error': 'Username already exists'}

        # Continue with user creation if the username is unique
        res = udb.execute('SELECT MAX(user_id) FROM users')
        user_id = res.fetchone()[0] + 1
        guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id)) # NOTE: generating guid from user_id because game object pulled from stats.db don't have username in them, only user_id, and joining stats.db.games with users table would be too much of a hassle and I don't want to  redesign the DB 
        print('GUID: ', guid)
        udb.execute('INSERT INTO users(guid, user_id, username) VALUES(?,?,?)', 
                    [str(guid), user_id, username])
        udb.commit()

        # row = udb.execute('SELECT * FROM users WHERE username=?', [username])       # Debugging
        # print('Newly created user: ', row.fetchone())
        
        gamesdb = (g1, g2, g3)
        gdb = gamesdb[int(guid) % 3]

        # row = gdb.execute('SELECT * FROM users WHERE username=?', [username])       # Debugging
        # print('Before inserting user: ', row.fetchone())
        
        gdb.execute('INSERT INTO users(guid, user_id, username) VALUES(?,?,?)',
                    [str(guid), user_id, username])
        gdb.commit()

        # row = gdb.execute('SELECT * FROM users WHERE username=?', [username])       # Debugging
        # print('After inserting user: ', row.fetchone())

        return {'Success' : 'User created', 
                'user': {
                    'guid': str(guid), 
                    'user_id': user_id, 
                    'username': username
                }}
    except sqlite3.IntegrityError as e:
        return {'Error' : 'User already exists', 
                'user': {
                    'guid': str(guid), 
                    'user_id': user_id,
                    'username': username
                }}
    except Exception as e:
        return {'Error' : e}