
DROP TABLE IF EXISTS LiveGames;
CREATE TABLE LiveGames(
  user_id INT,
  game_id INT,
  guesses_remain int,
  guess1 CHAR(5),
  guess2 CHAR(5),
  guess3 CHAR(5),
  guess4 CHAR(5),
  guess5 CHAR(5),
  guess6 CHAR(5),
  PRIMARY KEY (user_id, game_id)
);
