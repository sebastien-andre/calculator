import json
import pytest

from calc.api.main import create_app


@pytest.fixture
def client():
    # Create test client
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_api_evaluate(client):
    response = client.post('/evaluate', 
        json={"expression": "2 + 3"},
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["result"] == "5"
    assert data["status"] == "success"


def test_api_evaluate_missing_expression(client):
    response = client.post('/evaluate', 
        json={},
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_api_evaluate_invalid_expression(client):
    response = client.post('/evaluate', 
        json={"expression": "2 + + 3"},
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["status"] == "error"


def test_api_evaluate_division_by_zero(client):
    response = client.post('/evaluate', 
        json={"expression": "10 / 0"},
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["status"] == "error"


def test_api_history(client):
    client.post('/evaluate', json={"expression": "5 + 5"}, content_type='application/json')
    client.post('/evaluate', json={"expression": "10 * 2"}, content_type='application/json')
    
    # Get history
    response = client.get('/history')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["history"]) == 2
    assert data["count"] == 2
    assert data["history"][0]["expression"] == "5 + 5"
    assert data["history"][0]["result"] == "10"


def test_api_clear_history(client):
    # Add some history
    client.post('/evaluate', json={"expression": "1 + 1"}, content_type='application/json')
    client.post('/evaluate', json={"expression": "2 + 2"}, content_type='application/json')
    
    # Clear it
    response = client.post('/clear')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    
    # Verify history is empty
    response = client.get('/history')
    data = json.loads(response.data)
    assert len(data["history"]) == 0


def test_api_reset(client):
    # Add some history
    client.post('/evaluate', json={"expression": "5 + 5"}, content_type='application/json')
    
    # Reset
    response = client.post('/reset')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    
    # Verify history is empty
    response = client.get('/history')
    data = json.loads(response.data)
    assert len(data["history"]) == 0


def test_api_operator_precedence(client):
    response = client.post('/evaluate', 
        json={"expression": "2 + 3 * 4"},
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["result"] == "14"


def test_api_parentheses(client):
    response = client.post('/evaluate', 
        json={"expression": "(2 + 3) * 4"},
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["result"] == "20"
