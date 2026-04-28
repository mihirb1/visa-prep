import pytest
from app import app

@pytest.fixture
def client():
    # sets up a fake "browser" to talk to Flask app

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_validate_endpoint_success(client):
    """Test that a valid POST request returns 200 OK."""
    payload = {"amount": 100.0, "merchant": "Apple", "country": "USA"}
    response = client.post('/validate', json=payload)

    assert response.status_code == 200
    assert response.get_json()["status"] == "Success"

def test_validate_endpoint_compliance_fail(client):
    """Test that a sanctioned country returns a 400 Security Alert."""
    payload = {"amount": 50.0, "merchant": "Cafe", "country": "Iran", "rate": 1.0}
    response = client.post("/validate", json=payload)

    assert response.status_code == 400
    assert "Security Alert" in response.get_json()["status"]

def test_validate_endpoint_small_transaction(client):
    """Test that a valid POST request returns 200 OK with minimal transaction amount."""
    payload = {"amount": 0.01, "merchant": "Frooti", "country": "India"}
    response = client.post("/validate", json=payload)

    assert response.status_code == 200
    assert response.get_json()["status"] == "Success"

def test_validate_endpoint_empty_merchant(client):
    """Test that a POST request returns a 400 Security Alert."""
    payload = {"amount": 20.5, "merchant": "", "country": "USA"}

    response = client.post('/validate', json=payload)
    assert response.status_code == 400
    assert response.get_json()["status"] == "Data Error"