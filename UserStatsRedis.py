# top 30 winners and streaks are stored in Redis

from fastapi import FastAPI, Depends
import contextlib
import datetime
import sqlite3
from pydantic import BaseModel#, BaseSettings
from pydantic_settings import BaseSettings
import json
import uuid
import redis

USER_DB = './var/users.db'
GAME1_DB = './var/game1.db'
GAME2_DB = './var/game2.db'
GAME3_DB = './var/game3.db'


class Result(BaseModel):
    guesses: int
    won: bool


class Settings(BaseSettings):
    user_db: str = USER_DB
    game1db: str = GAME1_DB
    game2db: str = GAME2_DB
    game3db: str = GAME3_DB

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


settings = Settings()
app = FastAPI()


@app.get("/")
def hello():
    return {"message": "hello world", "message2": "UserStatsRedis.py"}

# insert game into the correct shard based on guid for storage
@app.post("/stats/{user_id}/{game_id}")
def gameResult(user_id: int, game_id: int, result: Result, g1: sqlite3.Connection = Depends(get_db1), g2: sqlite3.Connection = Depends(get_db2), g3: sqlite3.Connection = Depends(get_db3)):
    try:
        gamedb = (g1, g2, g3)
        guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id))

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
@app.get('/stats/top-winners')
def getTopWinners():
  r = redis.Redis()
  top_wins = r.zrevrange('top_wins', 0, 9, withscores=True)
  
  return [(user_id.decode(), int(score)) for (user_id, score) in top_wins]

# return top 10 streaks
@app.get('/stats/top-streaks')
def getTopStreaks():
  r = redis.Redis()
  top_streaks = r.zrevrange('top_streaks', 0, 9, withscores=True)
  return [(user_id.decode(), int(score)) for (user_id, score) in top_streaks]

# return stats for a given user
@app.get('/stats/{userID}')
def getUserStats(userID: int, udb: sqlite3.Connection = Depends(get_db), g1: sqlite3.Connection = Depends(get_db1), g2: sqlite3.Connection = Depends(get_db2), g3: sqlite3.Connection = Depends(get_db3)):
    gamedb = (GAME1_DB, GAME2_DB, GAME3_DB)
    guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(userID))
    cursor = udb.cursor()
    cursor.execute('ATTACH DATABASE ' + "'" +
                   gamedb[int(guid) % 3] + "'" + ' AS ga')

    cursor.execute('''
        select  
            i.gamesPlayed,
            i.gamesWon,
	        (cast(i.gameswon as real)/cast(i.gamesplayed as real))*100 as winPercentage,
	        cast(i.guesses as real)/cast(i.gamesplayed as real) as averageGuesses,
	        s.streak as currentStreak, 
            i.maxStreak
        from
            (select 
                u.user_id,
                u.username,
                count(g.game_id) as gamesplayed, 
                w.[count(won)] as gameswon, 
                sum(g.guesses)as guesses,
                max(st.streak) as maxstreak
            from
	            main.users u
	            inner join ga.wins w on u.user_id=w.user_id
	            inner join ga.games g on w.user_id = g.user_id
	            left outer join streaks st on st.user_id=g.user_id
            where
	            u.user_id=(?)) i
	    left join streaks s on s.user_id = i.user_id
        order by beginning desc
        limit 1
        ''', (userID,))
    data_json = {}
    headers = [i[0] for i in cursor.description]
    data = cursor.fetchall()

    for row in data:
        for i, header in enumerate(headers):
            data_json.update({header: row[i]})

    guesses = {}
    gameguesses = cursor.execute(
        '''select guesses,count(*) as NoOfGames from ga.games where user_id=(?) group by guesses''', (userID,)).fetchall()
    for row in gameguesses:
        guesses.update({row[0]: row[1]})
    data_json.update({"guesses": guesses})
    return data_json

# return user_guid for a given username
@app.get('/stats')
def get_user_id(user_name: str, udb: sqlite3.Connection = Depends(get_db)):
    row = udb.execute('SELECT * FROM users WHERE username=?', [user_name])
    try:
        return row.fetchone()[0]
    except TypeError:
        return -1