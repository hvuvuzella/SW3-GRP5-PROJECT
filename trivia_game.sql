DROP DATABASE IF EXISTS trivia_game;
-- create database:
CREATE DATABASE trivia_game;

USE trivia_game;

-- create normalized tables:
CREATE TABLE players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(40) NOT NULL
);

-- every time API is called, 15 new questions are added, and they will have ID number from 1 - infinity (NOT 1 - 15 every time)
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    difficulty_level VARCHAR(10) NOT NULL,
    question_text VARCHAR(300) NOT NULL,
    correct_answer VARCHAR(100) NOT NULL,
    incorrect_answer_1 VARCHAR(100) NOT NULL,
    incorrect_answer_2 VARCHAR(100) NOT NULL,
    incorrect_answer_3 VARCHAR(100) NOT NULL
);

-- for the games table, there will be 15 rows of data per game, corresponding to 15 answers from player:
CREATE TABLE games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    question_id INT,
    player_answer VARCHAR(100), -- store the user's answer
    is_correct BOOLEAN, -- check if answer is correct
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- there will be one row of data added to the scoreboard table after every 1 game played
CREATE TABLE scoreboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    player_id INT,
    total_score INT,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- example of using UPDATE query (to adapt in Python BE later) to update scoreboard after each game
UPDATE scoreboard sb
SET total_score = (
    SELECT COUNT(*) 
    FROM games 
    WHERE id = sb.game_id AND is_correct = TRUE
);

-- example of using SELECT query to get top 10 scores to display on the Leaderboard
SELECT * 
FROM scoreboard
ORDER BY total_score DESC
LIMIT 10;
