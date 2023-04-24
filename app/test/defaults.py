import pytest
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

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client