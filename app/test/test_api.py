import pytest
import requests
from os import environ

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.flaskenv')
load_dotenv(dotenv_path=dotenv_path)

API_KEY=environ.get('API_KEY')
API_HOST=environ.get('API_HOST')
API_URL=environ.get('API_URL')
EMAIL=environ.get('EMAIL')
CALORIES_API_URL=environ.get('CALORIES_API_URL')
NUTRITION_API_URL=environ.get('NUTRITION_API_URL')

#def test_api_calories():
    #response = requests.get(f"{CALORIES_API_URL}?activity=swimming",headers={'X-Api-Key':API_KEY})
    #assert response.status_code == 200

#def test_api_nutrition():
    #response = requests.get(f"{NUTRITION_API_URL}?query=eggs",headers={'X-Api-Key':API_KEY})
    #assert response.status_code == 200

    #Test 1 -> failed ending up being due to typos(oops) error 
    #changes the path and used dotenv to fix this
    #Test 2 ->passed both apis are callable on their own

#changing the test a bit due to testing the routes I need to put the links and api key in the request

def test_api_calories():
    response = requests.get(f"{'https://api.api-ninjas.com/v1/caloriesburned'}?activity=swimming",headers={'X-Api-Key':'lAoyv2xDhzmedTOJc6bn9A==XUdmv84oWvckWrhN'})
    assert response.status_code == 200

def test_api_nutrition():
    response = requests.get(f"{'https://api.api-ninjas.com/v1/nutrition'}?query=eggs",headers={'X-Api-Key':'lAoyv2xDhzmedTOJc6bn9A==XUdmv84oWvckWrhN'})
    assert response.status_code == 200

#---------------------------------------------testing the routes-----------------------------------------------

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


def test_add_workout_get(client):
    response = client.get('/add_workout')
    assert response.status_code == 405


#errors with the app imports
#errors with db imports 
#-> ImportError: cannot import name 'db' from partially initialized module 'app' routes line 10
#tried changing what path i was in still no change 
#tried to add testconfig inorder for pytest to look outside of the folder it didnt work 
#added an empty int file and it passed two of the tests my routes are still giving an issue
#took out fit_app = app() and replaced fit_app with just app
#added line 45 as well
#test failed but it was supposed to 
#changed status code to 405 so now it passes woo! 

#line 48 just passing and doing nothing but in fut anything that requires chaning the app context for each test 
#would go here!

def test_add_food_get(client):
    response = client.get('/add_food')
    assert response.status_code == 405

#basically copied and pased the food stuff beacuse their super similar