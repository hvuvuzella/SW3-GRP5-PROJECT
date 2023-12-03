import unittest
import json

from app import app


class TestAppRoutes(unittest.TestCase):

    # Create a test client to make requests to Flask routes without running the server in a live environment
    def setUp(self):
        self.app = app.test_client()

    def test_add_game_route(self):
        # Mocking user_name for the test
        user_name = "helen"
        user_data = {"user_name": user_name}

        # Sending a POST request to the /check_answer route
        response = self.app.post('/add_new_game', json=user_data)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)

        # Check the format of response
        self.assertIn('player_id', data)
        self.assertIn('game_id', data)
        self.assertIn('question', data)

    def test_check_answer_route(self):

        # Mocking data for the test
        answer_data = {
            "game_id": 1,
            "answer": "Crypton Future Media",
            "question_id": 3
        }

        # Sending a PUT request to the /check_answer route
        response = self.app.put('/check_answer', json=answer_data)
        print(response.status_code)
        print(response.get_data(as_text=True))

        # self.assertEqual(response.status_code, 200)
        #
        # # Check the format of response
        # self.assertIn('score', response.get_data(as_text=True))
        # self.assertIn('correct_answer', response.get_data(as_text=True))
        # self.assertIn('result', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_next_question_route(self):
        # Mocking game_id for the test
        game_id = 1

        # Sending a GET request to the /next_question route
        response = self.app.get(f'/next_question/{game_id}')

        # Check the response
        if response.status_code == 200:
            self.assertIn('question', response.get_data(as_text=True))
        else:
            self.assertEqual(response.status_code, 404)

    def test_leaderboard_route(self):
        # Sending a GET request to the /leaderboard/ route
        response = self.app.get('/leaderboard/')

        # Check the response
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
