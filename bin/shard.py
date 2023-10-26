# used only during initial setup
# sharding the games table from stats.db into game1.db, game2.db, game3.db
# copying users from stats.db to users.db
# also create index for games.won to speed up the view creation for wins and streaks
import contextlib
import uuid
import sqlite3

DATABASE = './var/stats.db'
USERSDB = './var/users.db'
GAME1 = './var/game1.db'
GAME2 = './var/game2.db'
GAME3 = './var/game3.db'

with contextlib.closing(sqlite3.connect(DATABASE)) as stats:
    with contextlib.closing(sqlite3.connect(USERSDB)) as u:
        with contextlib.closing(sqlite3.connect(GAME1)) as g1:
            with contextlib.closing(sqlite3.connect(GAME2)) as g2:
                with contextlib.closing(sqlite3.connect(GAME3)) as g3:
                
                    sc = stats.cursor()
                    uc = u.cursor()
                    GAME_CONNECTIONS = (g1, g2, g3)
                    gc1 = g1.cursor()
                    gc2 = g2.cursor()
                    gc3 = g3.cursor()
                    GAME_CURSORS = [gc1, gc2, gc3]
                    [print(g) for g in GAME_CURSORS]
                    # GAME_CURSORS = [g.cursor() for g in GAME_CONNECTIONS]

                    # deleting existing tables and views
                    deleteExisting = ('DROP VIEW IF EXISTS wins','DROP VIEW IF EXISTS streaks;','DROP TABLE IF EXISTS games;','DROP TABLE IF EXISTS users;')
                    uc.execute('DROP TABLE IF EXISTS users;')
                    for cmd in deleteExisting:
                        for cursor in GAME_CURSORS:
                            cursor.execute(cmd)

                    # copying users from stats.db to users.db
                    uc.execute('CREATE TABLE users (guid GUID PRIMARY KEY, user_id INTEGER NOT NULL, username TEXT)')
                    for cursor in GAME_CURSORS:
                        cursor.execute('CREATE TABLE IF NOT EXISTS users (guid GUID PRIMARY KEY, user_id INTEGER NOT NULL, username TEXT)')
                    users = sc.execute('SELECT * FROM users').fetchall()
                    
                    game_shard_size = [0,0,0]   # number of values in game1.db, game2.db, game3.db
                    for user in users:

                        new_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user[0]))
                        if (user[0] == 1):
                            print('shard.py user object: ', user)
                            print('shard.py new_uuid: ', new_uuid)
                        uc.execute(
                            '''
                                INSERT INTO users(guid, user_id, username)
                                VALUES(?, ?, ?)
                            ''',
                            [str(new_uuid), user[0], user[1]]
                        )
                        GAME_CURSORS[int(new_uuid) % 3].execute(
                            '''
                                INSERT INTO users(guid, user_id, username)
                                VALUES(?, ?, ?)
                            ''',
                            [str(new_uuid), user[0], user[1]]
                        )

                    u.commit()

                    # copying/sharding games from stats.db to game1.db, game2.db, game3.db
                    gamesTable = 'CREATE TABLE games(guid GUID NOT NULL, user_id INTEGER NOT NULL, game_id INTEGER NOT NULL, finished DATE DEFAULT CURRENT_TIMESTAMP, guesses INTEGER, won BOOLEAN, PRIMARY KEY(guid, game_id), FOREIGN KEY(guid) REFERENCES users(guid))'
                    for cursor in GAME_CURSORS:
                        cursor.execute(gamesTable)
                    games = sc.execute('SELECT * FROM games').fetchall() 
                    for game in games:
                        # NOTE: game[0] is the guid, but we need username
                        # guid = game[0]
                        guid = uuid.uuid3(uuid.NAMESPACE_DNS, str(game[0]))

                        sqlcommand ="""
                                    INSERT INTO games(guid, user_id, game_id, finished, guesses, won)
                                    VALUES(?, ?, ?, ?, ?, ?)
                                    """
                        if (game[1] == 1):
                            print('shard.py ucohen game object: ', game)
                        GAME_CURSORS[int(guid) % 3].execute(sqlcommand, [str(guid), game[0], game[1], game[2], game[3], game[4]])
                        game_shard_size[int(guid) % 3] += 1
                        
                    sqlcommands = (
                        ## PROBLEM: attach works fine, can query Users table
                        ##          but cannot access Users while creating view
                        # """
                        #     ATTACH DATABASE './var/users.db' AS Users;
                        # """,
                        """
                            CREATE INDEX games_won_idx ON games(won);
                        """,
                        """
                            CREATE VIEW wins 
                            AS 
                                SELECT username, COUNT(won) 
                                FROM games g
                                JOIN Users u ON g.user_id=u.user_id
                                WHERE won=TRUE
                                GROUP BY u.user_id
                                ORDER BY COUNT(won) DESC;""",
                        """
                            CREATE VIEW streaks AS
                                WITH GameRows AS (
                                    SELECT 
                                        ROW_NUMBER() OVER (ORDER BY finished) as row_num, 
                                        g.user_id, 
                                        username, 
                                        finished, 
                                        won 
                                    FROM Games g 
                                    JOIN Users u ON g.user_id=u.user_id
                                    ORDER BY g.user_id, row_num
                                ),
                                RunGroups AS (
                                    SELECT 
                                        ng1.row_num, username, ng1.user_id, ng1.won, ng1.finished,
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
                                        username,
                                        user_id, 
                                        won, 
                                        MIN(finished) AS beginning, 
                                        MAX(finished) AS ending, 
                                        COUNT(*) AS streak
                                    FROM RunGroups
                                    GROUP BY user_id, won, RunGroup
                                    ORDER BY user_id, row_num
                                )
                                SELECT 
                                    username,
                                    user_id, 
                                    won, 
                                    beginning, 
                                    ending, 
                                    streak
                                FROM Streaks
                                WHERE won=1
                                ORDER BY streak DESC;
                        """
                    )
                    for cmd in sqlcommands:
                        for cursor in GAME_CURSORS:
                            cursor.execute(cmd)

                    ## not changing db (stats.db) so no need to commit
                    for conn in GAME_CONNECTIONS:
                        conn.commit()
                    print("G1: " + str(game_shard_size[0]) + ", G2: " + str(game_shard_size[1]) + ", G3: " + str(game_shard_size[2]))