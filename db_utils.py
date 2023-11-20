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


def set_question(difficulty_level, question_text, correct_answer, incorrect_answer_1, incorrect_answer_2,
                 incorrect_answer_3):
    try:
        db_name = 'trivia_game'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to database {db_name}")

        query = f"""
                    INSERT INTO `trivia_game`.`questions` (`difficulty_level`, `question_text`, `correct_answer`,
                        `incorrect_answer_1`, `incorrect_answer_2`, `incorrect_answer_3`)
                    VALUES ('{difficulty_level}', '{question_text}', '{correct_answer}',
                        '{incorrect_answer_1}', '{incorrect_answer_2}', '{incorrect_answer_3}')
                """

        cur.execute(query)
        db_connection.commit()
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if db_connection:
            db_connection.close()


if __name__ == '__main__':
    main()
