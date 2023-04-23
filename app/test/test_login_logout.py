import pytest
from os import environ

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.flaskenv')
load_dotenv(dotenv_path=dotenv_path)

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


def test_login_with_bad_credentials(client):
    response = client.post('/login', data=dict(
        username="bad_username",
        password="bad_password"
    ), follow_redirects=True)
    assert response.status_code == 401

def test_login_with_good_credentials(client):
    response = client.post('/login', data=dict(
        username="kb",
        password="csc400sp23"
    ), follow_redirects=True)
    assert response.status_code == 200

def test_login_logout(client):
    client.post('/login', data=dict(
        username="kb",
        password="csc400sp23"
    ), follow_redirects=True)

    assert len(client.cookie_jar) == 1

    client.get('/logout', follow_redirects=True)

    assert len(client.cookie_jar) == 0
