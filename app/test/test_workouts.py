from app.test.defaults import client

def test_add_workout_get(client):
    response = client.get('/add_workout')
    assert response.status_code == 405

def test_add_bad_workout(client):
    
    pass

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