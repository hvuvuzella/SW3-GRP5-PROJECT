import requests


def get_questions_from_api(amount, difficulty):
    url = f"https://opentdb.com/api.php?amount={amount}&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    return response.json()


# API request to retrieve standard set of 15 multiple-choice questions of any difficulty from API
def get_new_questions_from_api():
    url = f"https://opentdb.com/api.php?amount=15&type=multiple"
    response = requests.get(url)
    return response.json()
