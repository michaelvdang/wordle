import contextlib
import uuid
import sqlite3

DATABASE = './var/stats.db'
GAME1 = './var/game1.db'
GAME2 = './var/game2.db'
GAME3 = './var/game3.db'
USERSDB = './var/users.db'


with contextlib.closing(sqlite3.connect(DATABASE)) as db:
    with contextlib.closing(sqlite3.connect(GAME1)) as g1:
        with contextlib.closing(sqlite3.connect(GAME2)) as g2:
            with contextlib.closing(sqlite3.connect(GAME3)) as g3:
                with contextlib.closing(sqlite3.connect(USERSDB)) as u:
                
                    c = db.cursor()

                    gc1 = g1.cursor()
                    gc2 = g2.cursor()
                    gc3 = g3.cursor()
                    uc = u.cursor()
                    
                    deleteExisting = ('DROP VIEW IF EXISTS wins','DROP VIEW IF EXISTS streaks;','DROP TABLE IF EXISTS games;')
                    uc.execute('DROP TABLE IF EXISTS users;')
                    for cmd in deleteExisting:
                        gc1.execute(cmd)
                        gc2.execute(cmd)
                        gc3.execute(cmd)

                    gamesTable = 'CREATE TABLE games(guid GUID NOT NULL, user_id INTEGER NOT NULL, game_id INTEGER NOT NULL, finished DATE DEFAULT CURRENT_TIMESTAMP, guesses INTEGER, won BOOLEAN, PRIMARY KEY(guid, game_id), FOREIGN KEY(guid) REFERENCES users(guid))'
                    gc1.execute(gamesTable)
                    gc2.execute(gamesTable)
                    gc3.execute(gamesTable)

                    uc.execute('CREATE TABLE users (guid GUID PRIMARY KEY, user_id INTEGER NOT NULL, username TEXT)')
                    
                    users = c.execute('SELECT * FROM users').fetchall()
                    count1 = 0
                    count2 = 0
                    count3 = 0
                    for user in users:
                        new_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user[0]))
                        uc.execute(
                        '''
                        INSERT INTO users(guid, user_id, username)
                        VALUES(?, ?, ?)
                        ''',
                        [str(new_uuid), user[0], user[1]]
                        )
                    u.commit()
                    games = db.execute('SELECT * FROM games').fetchall() 
                    for game in games:
                        guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(game[0]))
                        
                        if (count1 % 10000 == 0):
                            print(str(count1) + ", " + str(count2) + ", " + str(count3))
                        sqlcommand ="""
                                    INSERT INTO games(guid, user_id, game_id, finished, guesses, won)
                                    VALUES(?, ?, ?, ?, ?, ?)
                                    """
                        if int(guid) % 3 == 0:
                            count1+=1
                            gc1.execute(sqlcommand, [str(guid), game[0], game[1], game[2], game[3], game[4]])
                            
                        elif int(guid) % 3 == 1:
                            count2+=1
                            gc2.execute(sqlcommand, [str(guid), game[0], game[1], game[2], game[3], game[4]])
                            
                        else:
                            count3+=1
                            gc3.execute(sqlcommand, [str(guid), game[0], game[1], game[2], game[3], game[4]])
                    sqlcommands =(
                            """
                            CREATE INDEX games_won_idx ON games(won)""",
                            """
                            CREATE VIEW wins
                            AS
                                SELECT
                                    user_id,
                                    COUNT(won)
                                FROM
                                    games
                                WHERE
                                    won = TRUE
                                GROUP BY
                                    user_id
                                ORDER BY
                                    COUNT(won) DESC""",
                            """
                            CREATE VIEW streaks
                            AS
                                WITH ranks AS (
                                    SELECT DISTINCT
                                        user_id,
                                        finished,
                                        RANK() OVER(PARTITION BY user_id ORDER BY finished) AS rank
                                    FROM
                                        games
                                    WHERE
                                        won = TRUE
                                    ORDER BY
                                        user_id,
                                        finished
                                ),
                                groups AS (
                                    SELECT
                                        user_id,
                                        finished,
                                        rank,
                                        DATE(finished, '-' || rank || ' DAYS') AS base_date
                                    FROM
                                        ranks
                                )
                                SELECT
                                    user_id,
                                    COUNT(*) AS streak,
                                    MIN(finished) AS beginning,
                                    MAX(finished) AS ending
                                FROM
                                    groups
                                GROUP BY
                                    user_id, base_date
                                HAVING
                                    streak > 1
                                ORDER BY
                                    streak DESC,
                                    user_id""")
                    for cmd in sqlcommands:
                        gc1.execute(cmd)
                        gc2.execute(cmd)
                        gc3.execute(cmd)

                    g1.commit()
                    g2.commit()
                    g3.commit()
                    print("G1: " + str(count1) + ", G2: " + str(count2) + ", G3: " + str(count3))