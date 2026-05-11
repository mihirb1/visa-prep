import pytest
from app import app

@pytest.fixture
def client():
    # sets up a fake "browser" to talk to Flask app

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# testing after adding merchant functionality, will check database too

# Valid examples, all should return {"success", "validated", (merchant_name), (merchant_id)}

def test_validate_endpoint_usa_transaction_success(client):
    """Test that a valid POST request returns 200 OK."""
    payload = {"amount": 67.67, "merchant": "Nike"}
    response = client.post("/validate", json=payload)

    assert response.status_code == 200
    assert response.get_json()["status"] == "Success"

def test_validate_endpoint_hollister_transaction_success(client):
    """Test that a valid POST request returns 200 OK."""
    # payload = {"amount": 4.20, "merchant": "Hollister", "country": "China", "rate": 2.83}
    payload = {"amount": 67.67, "merchant": "Hollister", "country": "China", "rate": 2.83}

    response = client.post("/validate", json=payload)

    assert response.status_code == 200
    assert response.get_json()["status"] == "Success"

def test_validate_endpoint_adidas_transaction_success(client):
    """Test that a valid POST request returns 200 OK."""
    payload = {"amount": 6.90, "merchant": "Adidas", "country": "Germany", "rate": 3.17}
    response = client.post("/validate", json=payload)

    assert response.status_code == 200
    assert response.get_json()["status"] == "Success"

def test_validate_endpoint_create_new_merchant(client):
    """Test that a valid POST request returns 200 OK."""
    payload = {"amount": 7.84, "merchant": "Fanatics"}
    response = client.post("/validate", json=payload)

    assert response.status_code == 200
    assert response.get_json()["status"] == "Success"

# # Invalid examples, wth various types of errors
def test_validate_endpoint_invalid_amount_error(client):
    """Test that a POST requesst returns a 400 Data Error"""
    payload = {"amount": -5, "merchant": "Nike"}
    response = client.post("/validate", json=payload)

    assert response.status_code == 400
    assert response.get_json()["status"] == "Data Error"

def test_validate_endpoint_invalid_merchant_type(client):
    """Test that a POST requesst returns a 400 Data Error"""
    payload = {"amount": 4.20, "merchant": 10}
    response = client.post("/validate", json=payload)

    assert response.status_code == 400
    assert response.get_json()["status"] == "Data Error"

def test_validate_endpoint_forbidden_country(client):
    """Test that a POST requesst returns a 400 Security Alert"""
    payload = {"amount": 2.3, "merchant": "LeGOAT JAMES", "country": "North Korea"}
    response = client.post("/validate", json=payload)

    assert response.status_code == 400
    assert response.get_json()["status"] == "Security Alert"

def test_validate_endpoint_risky_company(client):
    """Test that a POST requesst returns a 400 Security Alert"""
    payload = {"amount": 2.3, "merchant": "Alibaba", "country": "Istanbul", "rate": 2.3}
    response = client.post("/validate", json=payload)

    assert response.status_code == 400
    assert response.get_json()["status"] == "Security Alert"