import pytest
from flask import Flask
from app import app, db
from app.models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        # Create a test user
        user = User(email='test@example.com', password='password', fullname="TESTER", photo="")
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.drop_all()

def test_login(client):
    # Test successful login
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 200

    # Test invalid email
    response = client.post('/login', json={'email': 'invalid@example.com', 'password': 'password'})
    assert response.status_code == 401

    # Test invalid password
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'invalid'})
    assert response.status_code == 401