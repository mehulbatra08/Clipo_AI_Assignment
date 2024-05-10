import pytest
from app import app, db, VideoProject, User
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_project(client):
    # Simulate user registration and login
    register_data = {
        'username': 'testuser',
        'password': 'password123'
    }
    client.post('/register', json=register_data)
    
    login_data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = client.post('/login', json=login_data)
    access_token = json.loads(response.data)['access_token']

    # Create a project
    project_data = {
        'title': 'Test Project',
        'description': 'This is a test project'
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.post('/projects', json=project_data, headers=headers)

    assert response.status_code == 201
    assert 'id' in json.loads(response.data)

def test_get_projects(client):
    response = client.get('/projects')

    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)
