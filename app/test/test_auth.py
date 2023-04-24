from app.test.defaults import client

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
