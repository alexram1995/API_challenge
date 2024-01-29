import pytest
from app import app, db
from app.models import Users

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        # Create a test user
        user = Users(email='test@example.com', password='password', fullname="TESTER", photo="")
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.drop_all()
        
def test_get_user(client):
    # Log them in to get an access token
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    access_token = response.json['access_token']
    user_id = response.json['user_id']

    # Test successful user retrieval
    response = client.get(f'/users/{user_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200

    # Test invalid user id
    response = client.get('/users/999', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404


def test_update_user(client):
    # Log them in to get an access token
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    access_token = response.json['access_token']
    user_id = response.json['user_id']

    # Test successful user update
    response = client.put(f'/users/{user_id}', json={'fullname': 'New Name'}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['fullname'] == 'New Name'

    # Test invalid user id
    response = client.put('/users/999', json={'fullname': 'New Name'}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404

def test_delete_user(client):
    # Log them in to get an access token
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    access_token = response.json['access_token']
    # Create a test user
    response = client.post('/register', json={'email': 'another@example.com', 'password': 'password', 'fullname': 'TESTER', 'photo': ''}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    user_id = response.json['id']
    print(response.json.items())
    # Delete the test user
    deleted = client.delete(f'/users/{user_id}', headers={'Authorization': f'Bearer {access_token}'})
    print(deleted.json.items())
    assert deleted.status_code == 200

    # Verify that the user was deleted
    response = client.get(f'/users/{user_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404