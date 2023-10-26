# top 30 winners and streaks are stored in Redis

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

REDISCLI_AUTH_PASSWORD = os.environ.get('REDISCLI_AUTH_PASSWORD')
def get_redis():
    yield redis.Redis(host='redis', 
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

    ## leaving this will throw an error because we have another .env
    # class Config():
    #     env_file = '.env'


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
    # "http://localhost:8080",
    "http://localhost:5173",    # needs this even when React App is local and Orc is remote
    "http://localhost:9100",
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
    return {"message": "hello world", "message2": "UserStatsRedis.py"}

# insert finished game into the correct shard based on guid for storage
@app.post("/stats/games/store-result", status_code=201)
def store_game_result(
        username: str, 
        user_id: int, 
        game_id: int, 
        result: Result, 
        g1: sqlite3.Connection = Depends(get_db1), 
        g2: sqlite3.Connection = Depends(get_db2), 
        g3: sqlite3.Connection = Depends(get_db3)):
    try:
        gamedb = (g1, g2, g3)
        guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id)) # NOTE: generating guid from user_id because game object pulled from stats.db don't have username in them, only user_id, and joining stats.db.games with users table would be too much of a hassle and I don't want to  redesign the DB 
        print('guid: ', guid)
        if (username == 'ucohen'):
            print('STATS ucohen guid: ', guid)
            print('STATS shard number: ', int(guid) % 3)

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
        return {'Success' : 'Game recorded'}

    except sqlite3.IntegrityError:
        return 'Integrity error, there is another game with this game_id'

# return top 10 winners
@app.get('/stats/top-winners', status_code=200)
def get_top_winners(r: redis.Redis = Depends(get_redis)):
    # r = redis.Redis('redis://redis:6379')
    # r = aioredis.from_url(config.redis_url, decode_responses=True)
    top_wins = r.zrevrange('top_wins', 0, 9, withscores=True)
    
    return [(user_id, int(score)) for (user_id, score) in top_wins]

# return top 10 streaks
@app.get('/stats/top-streaks', status_code=200)
def get_top_streaks(r: redis.Redis = Depends(get_redis)):
    # r = redis.Redis('redis://redis:6379')
    # r = aioredis.from_url(config.redis_url, decode_responses=True)
    top_streaks = r.zrevrange('top_streaks', 0, 9, withscores=True)
    return [(user_id, int(score)) for (user_id, score) in top_streaks]

@app.get('/stats/top_streaks_and_winners', status_code=200)
def get_top_streaks_and_winners(r: redis.Redis = Depends(get_redis)):
    top_wins = r.zrevrange('top_wins', 0, 9, withscores=True)
    top_streaks = r.zrevrange('top_streaks', 0, 9, withscores=True)
    return {'top_wins': top_wins, 'top_streaks': top_streaks}

# return stats for a given user
@app.get('/stats/users', status_code=200)
def get_user_stats(
        username: str,
        user_id: int, 
        udb: sqlite3.Connection = Depends(get_udb), 
        g1: sqlite3.Connection = Depends(get_db1), 
        g2: sqlite3.Connection = Depends(get_db2), 
        g3: sqlite3.Connection = Depends(get_db3)):
    gamedb = (g1, g2, g3)
    guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id)) # NOTE: generating guid from user_id because game object pulled from stats.db don't have username in them, only user_id, and joining stats.db.games with users table would be too much of a hassle and I don't want to  redesign the DB 
    print('guid: ', guid)
    gc = gamedb[int(guid) % 3 == 0].cursor()
    # games = gc.execute('select * from games limit 10;').fetchall()
    games = gc.execute("select *, (select max(streak) from streaks where user_id=8) from games where user_id=8 order by finished;").fetchall()
    print(games)
    return {'games': games}


    # current streak
    #   use RunGroup and get the last group, check if won or lost
    # max streak 
    #   select *, (select max(streak) from streaks where user_id=8) from games where user_id=8 order by finished;

    
    
    
    # cursor = udb.cursor()
    # cursor.execute('ATTACH DATABASE ' + "'" +
    #                gamedb[int(guid) % 3] + "'" + ' AS ga')

    # cursor.execute('''
    #     select  
    #         i.gamesPlayed,
    #         i.gamesWon,
	#         (cast(i.gameswon as real)/cast(i.gamesplayed as real))*100 as winPercentage,
	#         cast(i.guesses as real)/cast(i.gamesplayed as real) as averageGuesses,
	#         s.streak as currentStreak, 
    #         i.maxStreak
    #     from
    #         (select 
    #             u.user_id,
    #             u.username,
    #             count(g.game_id) as gamesplayed, 
    #             w.[count(won)] as gameswon, 
    #             sum(g.guesses)as guesses,
    #             max(st.streak) as maxstreak
    #         from
	#             main.users u
	#             inner join ga.wins w on u.user_id=w.user_id
	#             inner join ga.games g on w.user_id = g.user_id
	#             left outer join streaks st on st.user_id=g.user_id
    #         where
	#             u.user_id=(?)) i
	#     left join streaks s on s.user_id = i.user_id
    #     order by beginning desc
    #     limit 1
    #     ''', (userID,))
    # data_json = {}
    # headers = [i[0] for i in cursor.description]
    # data = cursor.fetchall()

    # for row in data:
    #     for i, header in enumerate(headers):
    #         data_json.update({header: row[i]})

    # guesses = {}
    # gameguesses = cursor.execute(
    #     '''select guesses,count(*) as NoOfGames from ga.games where user_id=(?) group by guesses''', (userID,)).fetchall()
    # for row in gameguesses:
    #     guesses.update({row[0]: row[1]})
    # data_json.update({"guesses": guesses})
    # data_json.update({'user_id': userID})
    # return data_json

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
def create_user(username: str, udb: sqlite3.Connection = Depends(get_udb)):
    try:
        # check that username is unique
        row = udb.execute('SELECT * FROM users WHERE username=?', [username])
        existing_user = row.fetchone()
        if existing_user:
            return {'Error': 'Username already exists'}

        # Continue with user creation if the username is unique
        res = udb.execute('SELECT count(*) FROM users')
        user_id = res.fetchone()[0] + 1
        guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id)) # NOTE: generating guid from user_id because game object pulled from stats.db don't have username in them, only user_id, and joining stats.db.games with users table would be too much of a hassle and I don't want to  redesign the DB 
        print('GUID: ', guid)
        udb.execute('INSERT INTO users(guid, user_id, username) VALUES(?,?,?)', 
                    [str(guid), user_id, username])
        udb.commit()
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