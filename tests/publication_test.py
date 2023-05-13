import pytest
from flask import Flask
from app import app, db
from app.models import User, Publication

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        user = User(email='test@example.com', password='password', fullname="TESTER", photo="")
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.drop_all()


def test_post_publications(client):
    # Create a test user and log them in to get an access token
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    access_token = response.json['access_token']

    # Test successful publication creation
    response = client.post('/publications', json={'title': 'Test Title', 'description': 'Test Description', 'priority': 1, 'status': 'open'}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200

    # Test invalid request body
    response = client.post('/publications', json={}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 400

def test_get_all_publications_for_user(client):
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    access_token = response.json['access_token']
    # Create a test publication
    publication = Publication(title='Test Title', description='Test Description', priority=1, status='open', user_id=response.json['user_id'])
    with app.app_context():
        db.session.add(publication)
        db.session.commit()

    # Test getting all publications for user
    response = client.get('/publications', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200

def test_update_existing_publication(client):
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    access_token = response.json['access_token']

    # Create a test publication
    publication = client.post('/publications', json={'title': 'Test Title', 'description': 'Test Description', 'priority': 1, 'status': 'open'}, headers={'Authorization': f'Bearer {access_token}'})
    

    # Test successful publication update
    response = client.put(f'/publications/{publication.json["id"]}', json={'title': 'Updated Title', 'description': 'Updated Description', 'priority': 2, 'status': 'closed'}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200

    # Test invalid request body
    response = client.put(f'/publications/{publication.json["id"]}', json={}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 400

def test_delete_publication(client):
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    access_token = response.json['access_token']

    # Create a test publication
    publication = client.post('/publications', json={'title': 'Test Title', 'description': 'Test Description', 'priority': 1, 'status': 'open'}, headers={'Authorization': f'Bearer {access_token}'})

    # Test successful publication deletion
    response = client.delete(f'/publications/{publication.json["id"]}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200