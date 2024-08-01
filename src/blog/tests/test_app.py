import pytest
from app import app, db, Blog
import jwt
import datetime

SECRET_KEY = 'yoursecretkey'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def generate_token(user_id):
    token = jwt.encode({'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY)
    return token

def test_get_blogs(client):
    rv = client.get('/blogs')
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_create_blog(client):
    token = generate_token(1)
    rv = client.post('/blogs', headers={'x-access-tokens': token}, json={'title': 'test blog', 'content': 'test content'})
    assert rv.status_code == 200
    assert rv.get_json() == {'message': 'Blog created!'}

    rv = client.get('/blogs')
    assert rv.status_code == 200
    blogs = rv.get_json()
    assert len(blogs) == 1
    assert blogs[0]['title'] == 'test blog'
    assert blogs[0]['content'] == 'test content'

def test_delete_blog(client):
    token = generate_token(1)
    client.post('/blogs', headers={'x-access-tokens': token}, json={'title': 'test blog', 'content': 'test content'})
    
    rv = client.get('/blogs')
    blogs = rv.get_json()
    blog_id = blogs[0]['id']

    rv = client.delete(f'/blogs/{blog_id}', headers={'x-access-tokens': token})
    assert rv.status_code == 200
    assert rv.get_json() == {'message': 'Blog deleted!'}

    rv = client.get('/blogs')
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_update_blog(client):
    token = generate_token(1)
    client.post('/blogs', headers={'x-access-tokens': token}, json={'title': 'test blog', 'content': 'test content'})
    
    rv = client.get('/blogs')
    blogs = rv.get_json()
    blog_id = blogs[0]['id']

    rv = client.put(f'/blogs/{blog_id}', headers={'x-access-tokens': token}, json={'title': 'updated blog', 'content': 'updated content'})
    assert rv.status_code == 200
    assert rv.get_json() == {'message': 'Blog updated!'}

    rv = client.get('/blogs')
    blogs = rv.get_json()
    assert len(blogs) == 1
    assert blogs[0]['title'] == 'updated blog'
    assert blogs[0]['content'] == 'updated content'
