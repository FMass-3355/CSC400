from app.test.defaults import client
from app import otp

def test_create_user_and_verify(client):
    new_user = dict(
        username="kb2",
        password="csc400sp23",
        email="k.bevis02@gmail.com",
        fname="kari",
        lname="bevis",
        date_of_birth="1997-04-28",
        gender="Female"
    )

    response = client.post('/create_user', data=new_user, follow_redirects=True)
    assert response.get_data(as_text=True).find("OTP Verification") != -1
    
    response = client.post(f"/validate/{new_user.get('username')}/{new_user.get('password')}/{new_user.get('email')}/{new_user.get('fname')}/{new_user.get('lname')}/{new_user.get('date_of_birth')}/{new_user.get('gender')}/{new_user.get('regular')}", data=dict(otp=str(otp)))
    assert response.get_data(as_text=True).find("Email  verification is  successful") != -1