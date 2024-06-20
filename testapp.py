import pytest
import json
from app import app, users  # Assuming app and users are imported correctly

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = json.loads(response.data)
    assert len(data) == len(users), f"Expected {len(users)} users but got {len(data)}"

def test_get_user_by_id(client):
    response = client.get('/users/1')
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = json.loads(response.data)
    assert data['name'] == 'Alice', f"Expected user name 'Alice' but got {data['name']}"

    response = client.get('/users/999')
    assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"
    data = json.loads(response.data)
    assert data['error'] == 'User not found', f"Expected error message 'User not found' but got {data['error']}"
