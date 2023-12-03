import random
import unittest
from unittest.mock import MagicMock, patch
from db_utils import (
    get_or_add_player_id,
    add_new_game,
    add_new_questions,
    display_question_to_player,
    display_question_to_player_fifty_fifty,
    get_correct_answer,
    update_game_score,
    get_user_score,
    get_leaderboard
)


class TestGetOrAddPlayerId(unittest.TestCase):
    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_existing_player(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock()  # for database interactions, use mocking to replace actual database calls with
        # mock objects
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        mock_cursor.fetchone.return_value = (1,)

        # Test with the mocked database connection for an existing player
        existing_username = 'helenvu'
        existing_result = get_or_add_player_id(existing_username)

        # Check that the result is as expected
        self.assertEqual(existing_result, 1)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_player(self, mock_connect):
        mock_connection_new = MagicMock()
        mock_cursor_new = MagicMock()
        mock_cursor_new.fetchone.return_value = None  # Simulate that the player doesn't exist
        mock_cursor_new.lastrowid = 2  # Set lastrowid for the new player
        mock_connection_new.cursor.return_value = mock_cursor_new
        mock_connect.return_value = mock_connection_neweturn_value = mock_connection_new

        # Test with the mocked database connection
        new_username = 'paul'
        new_result = get_or_add_player_id(new_username)

        #  Check that the result is as expected
        self.assertEqual(new_result, 2)  # Assuming the new player gets player_id (doesn't work as expected as test
        # return random virtual ID)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_invalid_empty_username(self, mock_connect):
        # Set up the mock behavior for an invalid case
        mock_connection_invalid = MagicMock()
        mock_cursor_invalid = MagicMock()
        mock_cursor_invalid.fetchone.return_value = None  # Simulate that the player doesn't exist
        mock_cursor_invalid.lastrowid = -1  # Set lastrowid for the invalid case
        mock_connection_invalid.cursor.return_value = mock_cursor_invalid
        mock_connect.return_value = mock_connection_invalid

        # Test with the mocked database connection for an invalid case
        invalid_username = ''  # Invalid username (empty string)
        invalid_result = get_or_add_player_id(invalid_username)

        # Check that the result is as expected (e.g., -1 or any indicator for an invalid case)
        self.assertEqual(invalid_result, -1)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_exceeds_username_limit(self, mock_connect):
        # Set up the mock behavior for the case where the username exceeds the limit
        mock_connection_invalid = MagicMock()
        mock_cursor_invalid = MagicMock()
        mock_cursor_invalid.fetchone.return_value = None  # Simulate that the player doesn't exist
        mock_cursor_invalid.lastrowid = -1  # Set lastrowid for the invalid case
        mock_connection_invalid.cursor.return_value = mock_cursor_invalid
        mock_connect.return_value = mock_connection_invalid

        # Test with the mocked database connection for the case where the username exceeds the limit
        invalid_username = 'a' * 41  # Username with 41 characters, exceeding the 40-character limit
        invalid_result = get_or_add_player_id(invalid_username)

        # Check that the result is as expected (e.g., -1 or any indicator for an invalid case)
        self.assertEqual(invalid_result, -1)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')


class TestAddNewGame(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_game(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 17  # Mock the last inserted row ID
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection
        user_id = 3  # Assuming user_id 1 (replace as needed)
        game_id = add_new_game(user_id)

        # Assertions:
        # Check that the result is as expected
        self.assertEqual(game_id, 17)  # Assuming the last inserted row ID is 17

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was called on the mock_cursor to insert a new game
        insert_query = "INSERT INTO games (user_id, score) VALUES (%s, 0)"
        expected_values = (user_id,)
        mock_cursor.execute.assert_called_once_with(insert_query, expected_values)

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_invalid_user_id(self, mock_connect):
        # Set up the mock behavior for an invalid user_id
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Configure the cursor mock to return None when lastrowid is accessed
        mock_cursor.lastrowid = None

        # Test with the mocked database connection for an invalid user_id
        user_id = 'invalid_user_id'  # Invalid user_id (non-integer)
        game_id = add_new_game(user_id)

        # Assertions:
        # Check that the result is None for an invalid user_id
        self.assertIsNone(game_id)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was called on the mock_cursor due to the invalid user_id
        mock_cursor.execute.assert_called_once_with('INSERT INTO games (user_id, score) VALUES (%s, 0)',
                                                    (user_id,))

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_database_error(self, mock_connect):
        # Set up the mock behavior for a database error
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.side_effect = Exception('Database error')  # Simulate a database error
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection for a database error
        user_id = 4
        game_id = add_new_game(user_id)

        # Assertions:
        # Check that the result is None for a database error
        self.assertIsNone(game_id)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was not called on the mock_cursor due to the simulated database error
        mock_cursor.execute.assert_not_called()

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_connection_error(self, mock_connect):
        # Set up the mock behavior for a connection error
        mock_connect.side_effect = Exception('Connection error')  # Simulate a connection error

        # Test with the mocked database connection for a connection error
        user_id = 5
        game_id = add_new_game(user_id)

        # Assertions:
        # Check that the result is None for a connection error
        self.assertIsNone(game_id)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')


class TestAddNewQuestions(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_questions(self, mock_connect):
        # Mocking the database connection and cursor
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking the execute method to avoid actual database operations
        mock_cursor.execute.return_value = None

        # Input values for the function
        game_id = 1
        question_text = "What is the capital of France?"
        correct_answer = "Paris"
        incorrect_answers = ["Berlin", "Madrid", "Rome"]

        # Call the function
        add_new_questions(game_id, question_text, correct_answer, incorrect_answers)

        # Assertions
        mock_connect.assert_called_once_with('trivia_game')  # Assuming 'trivia_game' is the expected database name
        mock_connection.cursor.assert_called_once()

        expected_query = """
                INSERT INTO questions (
                    game_id,
                    question,
                    correct_answer,
                    answer_1,
                    answer_2,
                    answer_3,
                    is_provided
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        expected_values = (game_id, question_text, correct_answer, incorrect_answers[0], incorrect_answers[1],
                           incorrect_answers[2], False)
        mock_cursor.execute.assert_called_once_with(expected_query, expected_values)

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()


class TestDisplayQuestionToPlayer(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_display_question_to_player(self, mock_connect):
        # Mocking the database connection and cursor
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking the execute method to avoid actual database operations
        mock_cursor.execute.return_value = None

        # Mocking the fetchone method to simulate a question being returned
        mock_cursor.fetchone.return_value = (
            1, 1, "What is the capital of France?", "Paris", "Berlin", "Madrid", "Rome"
        )

        # Input values for the function
        game_id = 1

        # Mocking random.sample to ensure predictable shuffling for testing
        with patch('random.sample', side_effect=lambda data, k: data[:k]):
            # Call the function
            result = display_question_to_player(game_id)

        # Assertions
        mock_connect.assert_called_once_with('trivia_game')  # Assuming 'trivia_game' is the expected database name
        mock_connection.cursor.assert_called_once()

        # Check the first execute call for the SELECT query
        expected_query_select = """
            SELECT id, game_id, question, correct_answer, answer_1, answer_2, answer_3
            FROM questions
            WHERE game_id = %s
            AND is_provided = False
            LIMIT 1
        """
        expected_values_select = (game_id,)
        mock_cursor.execute.assert_any_call(expected_query_select, expected_values_select)

        # Check the second execute call for the UPDATE query
        expected_query_update = """
                UPDATE questions
                SET is_provided = True
                WHERE id = %s
            """
        expected_values_update = (1,)  # Assuming the question_id is always 1 for this test
        mock_cursor.execute.assert_any_call(expected_query_update, expected_values_update)

        # Additional assertions
        mock_cursor.fetchone.assert_called_once()

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

        # Additional assertions for the returned result with shuffled answers
        expected_result = {
            "question_id": 1,
            "game_id": 1,
            "question_text": "What is the capital of France?",
            "answers": ["Berlin", "Madrid", "Paris", "Rome"]  # Adjusted to the shuffled order
        }
        self.assertEqual(result["question_id"], expected_result["question_id"])
        self.assertEqual(result["game_id"], expected_result["game_id"])
        self.assertEqual(result["question_text"], expected_result["question_text"])

        # Use assertCountEqual to check if the answers are the same regardless of order
        self.assertCountEqual(result["answers"], expected_result["answers"])

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_no_more_questions(self, mock_connect):
        # Mocking the database connection and cursor for the case where there are no more questions
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking the execute method to simulate no more questions being returned
        mock_cursor.fetchone.return_value = None

        # Input values for the function
        game_id = 1

        # Call the function
        result = display_question_to_player(game_id)

        # Assertions for the case where there are no more questions
        mock_connect.assert_called_once_with('trivia_game')  # Assuming 'trivia_game' is the expected database name
        mock_connection.cursor.assert_called_once()

        # Check the execute call for the SELECT query
        expected_query_select = """
            SELECT id, game_id, question, correct_answer, answer_1, answer_2, answer_3
            FROM questions
            WHERE game_id = %s
            AND is_provided = False
            LIMIT 1
        """
        expected_values_select = (game_id,)
        mock_cursor.execute.assert_called_once_with(expected_query_select, expected_values_select)

        # Additional assertions for the returned result when there are no more questions
        expected_result = {"error": "No more questions"}
        self.assertEqual(result, expected_result)

        # Additional assertions for no further interactions with the cursor and connection
        mock_cursor.fetchone.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_shuffling_order(self, mock_connect):
        # Mocking the database connection and cursor
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking the execute method to avoid actual database operations
        mock_cursor.execute.return_value = None

        # Mocking the fetchone method to simulate a question being returned
        mock_cursor.fetchone.return_value = (
            1, 1, "What is the capital of France?", "Paris", "Berlin", "Madrid", "Rome"
        )

        # Input values for the function
        game_id = 1

        # Call the function
        result = display_question_to_player(game_id)

        # Assertions
        mock_connect.assert_called_once()  # Assuming 'trivia_game' is the expected database name
        mock_connection.cursor.assert_called_once()

        # Check the execute call for the SELECT query
        expected_query_select = """
            SELECT id, game_id, question, correct_answer, answer_1, answer_2, answer_3
            FROM questions
            WHERE game_id = %s
            AND is_provided = False
            LIMIT 1
        """
        expected_values_select = (game_id,)
        mock_cursor.execute.assert_any_call(expected_query_select, expected_values_select)

        # Check the execute call for the UPDATE query
        expected_query_update = """
                UPDATE questions
                SET is_provided = True
                WHERE id = %s
            """
        expected_values_update = (1,)  # Assuming the question_id is always 1 for this test
        mock_cursor.execute.assert_any_call(expected_query_update, expected_values_update)

        # Additional assertions
        mock_cursor.fetchone.assert_called_once()

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

        # Additional assertions for the returned result with shuffled answers
        expected_result = {
            "question_id": 1,
            "game_id": 1,
            "question_text": "What is the capital of France?",
            "answers": ["Berlin", "Madrid", "Paris", "Rome"]  # Adjusted to the shuffled order
        }
        self.assertEqual(result["question_id"], expected_result["question_id"])
        self.assertEqual(result["game_id"], expected_result["game_id"])
        self.assertEqual(result["question_text"], expected_result["question_text"])

        # Use assertCountEqual to check if the answers are the same regardless of order
        self.assertCountEqual(result["answers"], expected_result["answers"])


class TestGetLeaderboard(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_less_than_10_scores(self, mock_connect):
        # Mocking the database connection and cursor
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking the execute method to avoid actual database operations
        mock_cursor.execute.return_value = None

        # Mocking the fetchall method with less than 10 scores stored in database
        mock_cursor.fetchall.return_value = [
            ('user1', 10), ('user2', 9), ('user3', 8), ('user4', 7), ('user5', 6)
        ]

        # Call the function
        result = get_leaderboard()

        # Assertions
        self.assertEqual(result, [('user1', 10), ('user2', 9), ('user3', 8), ('user4', 7), ('user5', 6)])

        # Additional assertions
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
