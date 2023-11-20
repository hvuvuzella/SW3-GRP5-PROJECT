import requests


def get_questions_from_api(amount, difficulty):
    url = f"https://opentdb.com/api.php?amount={amount}&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    return response.json()
