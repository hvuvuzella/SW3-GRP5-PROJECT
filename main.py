import time

import requests

from api_utils import get_questions_from_api

from db_utils import get_or_add_player_id


class ConnectionError(Exception):
    pass


api_url = 'https://opentdb.com/api.php?amount={}&difficulty={}&type=multiple'


class Player:

    def __init__(self, name):
        self.name = name

    def get_or_create(self):
        user_id = get_or_add_player_id(self.name)
        return user_id


class Game:

    def __init__(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id

    def start_game(self):
        # to write a new game to a database
        # TODO: realise function set_game_to_database
        # set_game_to_database(user_id)

        # to get questions from the API
        self.set_questions()

        # to get a first question
        first_question = self.provide_question()
        return first_question

    # populate BW with questions from open API
    def set_questions_to_db(self, game_id, player_id):
        number_of_questions_per_difficulty = 5  # Set the desired number of questions
        questions = []
        for difficulty_level in ["easy", "medium", "hard"]:
            try:
                response = get_questions_from_api(number_of_questions_per_difficulty, difficulty_level)
                received_questions = response.get('results', [])
                questions.extend(received_questions)
                print(f"Received {len(received_questions)} questions for difficulty level {difficulty_level}")
                time.sleep(5)
            except Exception as err:
                raise ConnectionError(
                    f"Failed to get questions from API for difficulty {difficulty_level}. Error: {err}")

        url = f'http://127.0.0.1:5000/add_new_questions/{game_id}/{player_id}'
        headers = {'content-type': 'application/json'}
        data = {"results": questions}

        result = requests.post(url, headers=headers, json=data)

        return result.json()

    # TODO: if we decide to realise the functionality when player wants to take money and go
    # def finish_game(self):
    #     pass

    def check_answer(self, question_id, user_id):
        pass

    # request is sent to db to get the right answer for this question and question's value
    # the right answer is compared with the player's answer
    # user's score is got
    # if it is correct the score is increased and returned
    # if it is wrong the game is ended score in DB is set to zero and object with score zero is returned

    def provide_question(self):
        # TODO: make request to database which returns next question and answers with this game id and where used is false
        # TODO: it also has to to set this question's used field to true
        pass


class Lifeline:

    def provide_lifeline(self):
        pass


class Fifty_Fifty(Lifeline):
    def __init__(self, question_id):
        self.question_id = question_id

    def provide_lifeline(self):
        # request to database is made, and two wrong answers are sent and returned
        # front sees them and eliminates these two
        pass


class Phone(Lifeline):
    def __init__(self, question_id):
        self.question_id = question_id

    def provide_lifeline(self):
        pass
        # request to database is made, and correct and one wrong answer is sent back
        # one is randomly chosen out of two and sent to FE
        # front shows face of Bill Gates who says this answer


if __name__ == '__main__':
    game = Game(1, 1)
    game.set_questions_to_db(game.game_id, game.player_id)
