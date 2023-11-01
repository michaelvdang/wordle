PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS wins;
DROP VIEW IF EXISTS streaks;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE
);

CREATE INDEX username ON users(username);

CREATE TABLE games(
    user_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,
    finished DATE DEFAULT CURRENT_TIMESTAMP,
    guesses INTEGER,
    won BOOLEAN,
    PRIMARY KEY(user_id, game_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE INDEX games_won_idx ON games(won);

CREATE VIEW wins AS 
SELECT username, COUNT(won) 
FROM games g
JOIN users u ON g.user_id=u.user_id
WHERE won=TRUE
GROUP BY u.user_id
ORDER BY COUNT(won) DESC;


-- CREATE VIEW wins
-- AS
--     SELECT
--         user_id,
--         COUNT(won)
--     FROM
--         games
--     WHERE
--         won = TRUE
--     GROUP BY
--         user_id
--     ORDER BY
--         COUNT(won) DESC;

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

-- CREATE VIEW streaks
-- AS
--     WITH ranks AS (
--         SELECT DISTINCT
--             user_id,
--             finished,
--             RANK() OVER(PARTITION BY user_id ORDER BY finished) AS rank
--         FROM
--             games
--         WHERE
--             won = TRUE
--         ORDER BY
--             user_id,
--             finished
--     ),
--     groups AS (
--         SELECT
--             user_id,
--             finished,
--             rank,
--             DATE(finished, '-' || rank || ' DAYS') AS base_date
--         FROM
--             ranks
--     )
--     SELECT
--         user_id,
--         COUNT(*) AS streak,
--         MIN(finished) AS beginning,
--         MAX(finished) AS ending
--     FROM
--         groups
--     GROUP BY
--         user_id, base_date
--     HAVING
--         streak > 1
--     ORDER BY
--         user_id,
--         finished;

PRAGMA analysis_limit=1000;
PRAGMA optimize;