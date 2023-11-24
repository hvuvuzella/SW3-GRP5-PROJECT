import mysql.connector

def _connect_to_db(db_name):
    # Assuming you have a function to establish a database connection
    # Implement this function or replace it with your own connection logic

def set_question(difficulty_level, question_text, correct_answer, incorrect_answer_1, incorrect_answer_2,
                 incorrect_answer_3):
    try:
        db_name = 'trivia_game'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to database {db_name}")

        query = """
            INSERT INTO `trivia_game`.`questions` (`difficulty_level`, `question_text`, `correct_answer`,
                `incorrect_answer_1`, `incorrect_answer_2`, `incorrect_answer_3`)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (difficulty_level, question_text, correct_answer, incorrect_answer_1, incorrect_answer_2, incorrect_answer_3)

        cur.execute(query, values)
        db_connection.commit()

    except Exception as exc:
        print(exc)

    finally:
        if db_connection:
            db_connection.close()

# Example usage:
set_question("Easy", "What is the capital of France?", "Paris", "Berlin", "London", "Madrid")
