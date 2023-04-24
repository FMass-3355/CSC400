from app.test.defaults import client
import requests

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