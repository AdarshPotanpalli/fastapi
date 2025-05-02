from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest
from app import oauth2, models

#testing database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL) # establishing connection
TestingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine) # testing session

@pytest.fixture
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine) # this will ensure that we are able to see the data causing failed test
    db = TestingSessionLocal()
    try:
        yield db 
    finally: 
        db.close()

@pytest.fixture
def client(session):
    # function which overrides get_db for testing
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield session 
        finally: 
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db # must
    yield TestClient(app)

# for testing login, we temporaroly create a user, using fixture
@pytest.fixture()
def test_user(client):
    
    user_dict = {"email":"test@gmail.com", "password": "123456"}
    response = client.post("/users", json= user_dict)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_dict["password"]
    return new_user

@pytest.fixture()
def test_user2(client):
    
    user_dict = {"email":"test2@gmail.com", "password": "123456"}
    response = client.post("/users", json= user_dict)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_dict["password"]
    return new_user


@pytest.fixture
def token(test_user, client):
    jwt_token = oauth2.create_jwt_token(data = {"user_id": test_user['id']}) # gets the authentication token
    return jwt_token
    
# posting is done using client whose header should contain the token    
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client

# a fixture which creates test posts in the database w/o using app routes
@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post) 

    post_map = map(create_post_model, posts_data) # maps dict to orm model object
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts