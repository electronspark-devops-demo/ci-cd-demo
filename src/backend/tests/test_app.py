import pytest
from app import app, db, Item

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_get_items(client):
    rv = client.get('/items')
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_add_item(client):
    rv = client.post('/items', json={'name': 'test_item'})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['name'] == 'test_item'
    
    rv = client.get('/items')
    assert rv.status_code == 200
    assert len(rv.get_json()) == 1
    assert rv.get_json()[0]['name'] == 'test_item'
