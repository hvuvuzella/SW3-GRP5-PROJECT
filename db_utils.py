import mysql.connector  # module that allows to establish database connection
from config import USER, PASSWORD, HOST
import sys


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin="mysql_native_password",
        database=db_name
    )
    return connection


# Function which checks whether username exists and returns player_id,
# and if username does not exist, new username is added to players and returns new player_id:
def get_or_add_player_id(username):
    player_id = None

    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to check if player username exists
        check_query = "SELECT id FROM players WHERE username = %s"
        values = (username,)
        cur.execute(check_query, values)
        existing_player_id = cur.fetchone()

        if existing_player_id:
            # Player exists
            player_id = existing_player_id[0]
            print(f"Username '{username}' already exists in the database.")
            print(f"For existing username '{username}', player_id: {player_id}\n")
        else:
            # Player does not exist, add the new player
            add_query = "INSERT INTO players (username) VALUES (%s)"
            cur.execute(add_query, values)
            db_connection.commit()
            print("Player successfully added to DB!")

            # Get the ID of the last inserted row (player_id)
            player_id = cur.lastrowid
            print(f"For new username '{username}', new player_id: {player_id}\n")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")

    finally:
        if cur:
            # Close the cursor
            cur.close()
        if db_connection:
            # Close the connection
            db_connection.close()

        return {"player_id:": player_id}, player_id


# DB function to add new game to DB
def add_new_game(player_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'games' table
        query = """
                INSERT INTO games (
                    player_id
                ) VALUES (%s)
                """

        # values to be inserted
        values = (player_id,)

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print("Game successfully added to DB!")

        # Get the ID of the last inserted row (game_id)
        game_id = cur.lastrowid
        print(f"add_new_game function returns game_id: {game_id}\n")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}\n")
        game_id = None  # Set game_id to None in case of an error

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")
        game_id = None  # Set game_id to None in case of an error

    finally:
        if db_connection:
            # close the connection
            db_connection.close()

    return {"game_id:": game_id}, game_id


# DB function to add questions data to questions table in DB - will be used for API call
def add_new_question(game_id, player_id, difficulty_level, question_text, correct_answer, incorrect_answer_1,
                     incorrect_answer_2, incorrect_answer_3):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'questions' table
        query = """
                INSERT INTO questions (
                    game_id,
                    player_id,
                    difficulty_level,
                    question_text,
                    correct_answer,
                    incorrect_answer_1,
                    incorrect_answer_2,
                    incorrect_answer_3
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

        # Tuple containing the values to be inserted
        values = (
            game_id,
            player_id,
            difficulty_level,
            question_text,
            correct_answer,
            incorrect_answer_1,
            incorrect_answer_2,
            incorrect_answer_3
        )

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print(f"Question successfully added to DB!")

        # Get the last inserted ID (question_id)
        question_id = cur.lastrowid
        print(f"add_new_question function returns question_id: {question_id}\n")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}\n")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")

    finally:
        if db_connection:
            # close the connection
            db_connection.close()

    return {"question_id:": question_id}, question_id


# DB function to populate game_questions table with data at START of game:
# MAKE SURE TO: input player_answer = None, AND: input is_correct = None.
# The player_answer and is_correct columns will be updated later once player starts playing
def start_game_questions(game_id, player_id, question_id, player_answer, correct_answer, is_correct):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'game_questions' table
        query = """
                INSERT INTO game_questions (
                    game_id,
                    player_id,
                    question_id,
                    player_answer,
                    correct_answer,
                    is_correct
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """

        # Tuple containing the values to be inserted
        values = (
            game_id,
            player_id,
            question_id,
            player_answer,
            correct_answer,
            is_correct
        )

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print(f"Game question successfully added to DB!")

        # Get the last inserted ID (game_question_id)
        game_question_id = cur.lastrowid
        print(f"start_game_questions function returns game_question_id: {game_question_id}\n")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}\n")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")

    finally:
        if db_connection:
            # close the connection
            db_connection.close()

    return game_question_id


def start_game_scoreboard(game_id, player_id, total_score):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'scoreboard' table
        query = """
                INSERT INTO scoreboard (
                    game_id,
                    player_id,
                    total_score
                ) VALUES (%s, %s, %s)
                """

        # Tuple containing the values to be inserted
        values = (
            game_id,
            player_id,
            total_score
        )

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print(f"Initial start score of zero successfully added to DB!\n")

        # Get the last inserted ID (scoreboard_id)
        scoreboard_id = cur.lastrowid
        print(f"start_game_scoreboard function returns scoreboard_id: {scoreboard_id}\n")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}\n")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")

    finally:
        if db_connection:
            # close the connection
            db_connection.close()

    return scoreboard_id


# Define function to convert question data into dictionary for easier handling in main.py:
def question_dict(questions):
    question = []
    for i in questions:
        question.append(
            {
                "question_text": i[0],
                "correct_answer": i[1],
                "incorrect_answer_1": i[2],
                "incorrect_answer_2": i[3],
                "incorrect_answer_3": i[4]
            }
        )
    return question


def display_question_to_player(game_id, player_id, question_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the question details
        query = f"""
                SELECT question_text, correct_answer, incorrect_answer_1, incorrect_answer_2, incorrect_answer_3
                FROM questions
                WHERE game_id = {game_id}
                AND player_id = {player_id}
                AND id = {question_id}
            """
        cur.execute(query)
        results = cur.fetchall()
        cur.close()

        if results:
            question_displayed = question_dict(results)[0]
            print(f"question_id: {question_id}")
            print(question_displayed)
            print("Question fetched from DB!\n")
        else:
            print("Question not found in the database.\n")
            question_displayed = None

    except Exception:
        raise DbConnectionError("Failed to fetch question from DB\n")

    finally:
        if db_connection:
            db_connection.close()

    # Return the individual variables
    if question_displayed:
        question_text = question_displayed["question_text"]
        correct_answer = question_displayed["correct_answer"]
        incorrect_answer_1 = question_displayed["incorrect_answer_1"]
        incorrect_answer_2 = question_displayed["incorrect_answer_2"]
        incorrect_answer_3 = question_displayed["incorrect_answer_3"]

        print("Question Details:")
        print(f"question_text: {question_text}")
        print(f"correct_answer: {correct_answer}")
        print(f"incorrect_answer_1: {incorrect_answer_1}")
        print(f"incorrect_answer_2: {incorrect_answer_2}")
        print(f"incorrect_answer_3: {incorrect_answer_3}\n")

        return question_text, correct_answer, incorrect_answer_1, incorrect_answer_2, incorrect_answer_3
    else:
        return None


# Update game_questions with player_answer and evaluate whether is_correct is True (1) or False (0).
# The 1 and 0 also equals the points value which will be added in another function
def update_player_answer_is_correct(game_id, player_id, question_id, player_answer):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # Retrieve the correct answer for the given question from the game_questions table
        cur.execute("SELECT correct_answer FROM game_questions WHERE game_id = %s AND player_id = %s "
                    "AND question_id = %s",
                    (game_id, player_id, question_id))
        correct_answer_from_db = cur.fetchone()[0]

        # Compare player's answer with the correct answer and update is_correct
        is_correct = player_answer == correct_answer_from_db

        # SQL query for updating a row in the 'game_questions' table
        update_query = """
            UPDATE game_questions
            SET
                player_answer = %s,
                is_correct = %s
            WHERE
                game_id = %s
                AND player_id = %s
                AND question_id = %s
        """

        # Tuple containing the values to be updated
        values = (player_answer, is_correct, game_id, player_id, question_id)

        # Execute the update query with the provided values
        cur.execute(update_query, values)

        # Commit the changes to the database
        db_connection.commit()
        print("Game question updated successfully!\n")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}\n")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")

    finally:
        if db_connection:
            # Close the connection
            db_connection.close()


# DB function to update scoreboard after every question in the game, including after last question when game ends:
def update_scoreboard_total_score(game_id, player_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to update total_score in the scoreboard table
        update_query = """
                UPDATE scoreboard sb
                SET total_score = (
                    SELECT SUM(CAST(gq.is_correct AS SIGNED))
                    FROM game_questions gq
                    WHERE gq.game_id = sb.game_id AND gq.player_id = sb.player_id
                )
                WHERE sb.game_id = %s AND sb.player_id = %s
            """

        # Tuple containing the values for the WHERE clause
        values = (game_id, player_id)

        # Execute the update query with the provided values
        cur.execute(update_query, values)

        # Commit the changes to the database
        db_connection.commit()
        print("Total score updated successfully!\n")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")

    finally:
        if db_connection:
            # Close the connection
            db_connection.close()


# Define function to convert scoreboard data into dictionary for easier handling in main.py:
def total_score_dict(scores):
    score = []
    for i in scores:
        score.append(
            {
                "game_id": i[0],
                "player_id": i[1],
                "username": i[2],  # Assuming the username is the third column
                "total_score": i[3]  # Assuming the total_score is the fourth column
            }
        )
    return score


def display_total_score(game_id, player_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the total score and username for the specified game and player
        query = """
                SELECT s.game_id, s.player_id, p.username, s.total_score
                FROM scoreboard s
                JOIN players p ON s.player_id = p.id
                WHERE s.game_id = %s AND s.player_id = %s
            """
        cur.execute(query, (game_id, player_id))
        results = cur.fetchall()
        cur.close()

        if results:
            total_score_displayed = total_score_dict(results)[0]
            print(f"For Game ID {game_id}, Player ID {player_id}:")
            print(f"{total_score_displayed['username']} | TOTAL SCORE = {total_score_displayed['total_score']}\n")
        else:
            print(f"No total score found for Game ID {game_id}, Player ID {player_id}.\n")

    except Exception:
        raise DbConnectionError("Failed to fetch total score from DB\n")

    finally:
        if db_connection:
            db_connection.close()


# DB function to show Top 10 scores from scoreboard table - THIS ACTS AS THE LEADERBOARD
def get_leaderboard():
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor(dictionary=True)  # Use dictionary cursor for easier result handling
        print(f"Connected to database {db_name}")

        # SQL query to fetch the top 10 scores from the scoreboard with corresponding usernames
        query = """
            SELECT s.game_id, s.player_id, p.username, s.total_score
            FROM scoreboard s
            JOIN players p ON s.player_id = p.id
            ORDER BY s.total_score DESC
            LIMIT 10;
        """
        cur.execute(query)
        leaderboard_results = cur.fetchall()
        cur.close()

        leaderboard = []
        for result in leaderboard_results:
            leaderboard.append({
                "game_id": result["game_id"],
                "player_id": result["player_id"],
                "username": result["username"],
                "total_score": result["total_score"]
            })

        return leaderboard

    except Exception:
        raise DbConnectionError("Failed to fetch leaderboard from DB\n")

    finally:
        if db_connection:
            db_connection.close()


def main():
    # Run relevant functions below to ensure connecting to DB is successful:

    # Check if username exists, if exists, return player_id, if not, add new player and then return new player_id:
    get_or_add_player_id("helenvu")  # username exists
    get_or_add_player_id("marshmallow_squisher")  # username does not exist

    # Add a new game to DB when player starts game:
    add_new_game(2)

    # Add a new question to questions table including game_id and player_id as well:
    add_new_question(2, 2, "easy", "What is the capital of France?",
                     "Paris", "Berlin", "London",
                     "Madrid")

    # Load questions into game_questions table at start of game, with player answer and is_correct set to None
    # p.s. None in Python is equal to NULL in mySQL
    start_game_questions(2, 2, 4, None, "Paris", None)

    # Load scoreboard at start of game and set player's score to zero
    start_game_scoreboard(2, 2, 0)

    # Display question to user along with all 4 possible answers:
    display_question_to_player(2, 2, 4)

    # update game_questions with player_answer and evaluate whether is_correct at the same time
    game_id = 2  # Replace with the actual game_id
    player_id = 2  # Replace with the actual player_id
    question_id = 4  # Replace with the actual question_id
    player_answer = "Paris"  # Replace with the actual player's answer
    update_player_answer_is_correct(game_id, player_id, question_id, player_answer)

    # Update total_score in scoreboard after each question is answered:
    update_scoreboard_total_score(2, 2)

    # Display player's total_score in their game to player:
    display_total_score(2, 2)

    # Show Leaderboard (Top 10 scores of all time):
    leaderboard = get_leaderboard()
    print("Leaderboard:")
    for entry in leaderboard:
        print(entry)


if __name__ == '__main__':
    # main()
    get_or_add_player_id("Kate")

# COMMENTED OUT CODE WE MAY OR MAY NOT USE AGAIN:

# def display_question_to_player(game_id, player_id, id):  # id = id in 'questions' table
#     try:
#         # Establish a connection to the MySQL database
#         db_name = "trivia_game"
#         db_connection = _connect_to_db(db_name)
#         cur = db_connection.cursor()  # Create a cursor object to interact with the database
#         print(f"Connected to database {db_name}")
#
#         # SQL query for inserting a new row into the 'scoreboard' table
#         query = (f"""
#                 SELECT question_text, correct_answer, incorrect_answer_1, incorrect_answer_2, incorrect_answer_3
#                 FROM questions
#                 WHERE game_id = {game_id}
#                 AND player_id = {player_id}
#                 AND id = {id}
#                 """)
#         cur.execute(query)
#         results = cur.fetchall()
#         cur.close()
#         question_displayed = question_dict(results)
#         print(f"question_id: {id}")
#         print(f"{question_displayed}")
#         print("Question fetched from DB!\n")
#
#     except Exception:
#         raise DbConnectionError("Failed to fetch question from DB\n")
#
#     finally:
#         if db_connection:
#             db_connection.close()
#
#     return question_displayed


# def set_question(difficulty_level, question_text, correct_answer, incorrect_answer_1, incorrect_answer_2,
#                  incorrect_answer_3):
#     try:
#         db_name = "trivia_game"
#         db_connection = _connect_to_db(db_name)
#         cur = db_connection.cursor()
#         print(f"Connected to database {db_name}")
#
#         query = f"""
#                     INSERT INTO `trivia_game`.`questions` (`difficulty_level`, `question_text`, `correct_answer`,
#                         `incorrect_answer_1`, `incorrect_answer_2`, `incorrect_answer_3`)
#                     VALUES ('{difficulty_level}', '{question_text}', '{correct_answer}',
#                         '{incorrect_answer_1}', '{incorrect_answer_2}', '{incorrect_answer_3}')
#                 """
#
#         cur.execute(query)
#         db_connection.commit()
#         cur.close()
#
#     except mysql.connector.Error as err:
#         print(f"MySQL Error: {err}")
#
#     except Exception as exc:
#         print(f"An unexpected error occurred: {exc}")
#
#     finally:
#         if db_connection:
#             db_connection.close()


# # Define a function to a dd a new player and check if it exists to the players table
# def check_and_add_player(username, password):
#     try:
#         db_name = "trivia_game"
#         db_connection = _connect_to_db(db_name)
#         cursor = db_connection.cursor()
#
#         # Check if the player exists
#         query = "SELECT id, username FROM players WHERE username = %s and password = %s"
#         cursor.execute(query, (username, password))
#         existing_player = cursor.fetchone()
#
#         if existing_player:
#             # Player exists, return ID and username
#             player_id, existing_username = existing_player
#             print(f"Player {existing_username} with ID {player_id} already exists.\n")
#             return {"player_id": player_id, "username": existing_username}
#         else:
#             # Player does not exist, add a new player
#             insert_query = "INSERT INTO players (username, password) VALUES (%s, %s)"
#             data = (username, password)
#             cursor.execute(insert_query, data)
#             db_connection.commit()
#
#             new_player_id = cursor.lastrowid
#             print(f"New player {username} added with ID {new_player_id}.\n")
#             return {"player_id": new_player_id, "username": username}
#
#     except Exception:
#         raise DbConnectionError("Failed to insert data to DB")
#
#     finally:
#         if db_connection:
#             db_connection.close()
#             print("DB connection is closed")
