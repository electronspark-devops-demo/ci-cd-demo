import pytest
from app import app, db, User
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    rv = client.post('/register', json={'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com', 'avatar': 'http://example.com/avatar.png'})
    assert rv.status_code == 200
    assert rv.get_json() == {'message': 'registered successfully'}

def test_login(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com', 'avatar': 'http://example.com/avatar.png'})
    rv = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    assert rv.status_code == 200
    assert 'token' in rv.get_json()

def test_login_fail(client):
    rv = client.post('/login', json={'username': 'wronguser', 'password': 'wrongpass'})
    assert rv.status_code == 401
    assert rv.get_data(as_text=True) == 'Login failed!'

def test_get_user(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com', 'avatar': 'http://example.com/avatar.png'})
    login_response = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    token = login_response.get_json()['token']

    rv = client.get('/user', headers={'x-access-tokens': token})
    assert rv.status_code == 200
    user_data = rv.get_json()
    assert user_data['username'] == 'testuser'
    assert user_data['email'] == 'test@example.com'
    assert user_data['avatar'] == 'http://example.com/avatar.png'

def test_update_user(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com', 'avatar': 'http://example.com/avatar.png'})
    login_response = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    token = login_response.get_json()['token']

    rv = client.put('/user', headers={'x-access-tokens': token}, json={'email': 'new@example.com'})
    assert rv.status_code == 200
    assert rv.get_json() == {'message': 'user updated'}

    rv = client.get('/user', headers={'x-access-tokens': token})
    user_data = rv.get_json()
    assert user_data['email'] == 'new@example.com'
