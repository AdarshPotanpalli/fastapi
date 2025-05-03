import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_root(client):
    response = client.get("/")
    assert response.json().get('message') == "Hi this is Adarsh, cool, pushing to ubuntu server"
    assert response.status_code == 200
    
# testing the creation of user
def test_create_user(client, session):
    response = client.post("/users", json= {"email": "pytest@gmail.com", "password": "123456"})
    new_user = schemas.UserOut(**response.json()) # ** unpacks the json
    assert new_user.email == "pytest@gmail.com"
    assert response.status_code == 201
    
def test_login(client, test_user):
    response = client.post("/login", data= {"username": test_user["email"], "password": test_user["password"]}) # remember login was a form data
    
    #testing jwt token
    login_res = schemas.Token(**response.json()) # response model that we get after login
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms= [settings.algorithm]) # decoding the payload
    id = payload.get("user_id") # getting the user id from payload
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert response.status_code ==200
    
#testing incorrect login
@pytest.mark.parametrize("email, password, status", [
    ("test@gmail.com", "123456", 200),
    ("test@gmail.com", "wrongPassword", 403),
    ("wrongEmail@gmail.com", "123456", 403),
    ("test@gmail.com", None, 403),
    (None, "123456", 403)
])
def test_incorrect_login(test_user, client, email, password, status):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status