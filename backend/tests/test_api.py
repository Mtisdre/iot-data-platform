import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
from backend.app import app

def test_post_and_get_data():
    client = app.test_client()

    # Test POST request
    response = client.post("/data", json={"temperature": 25.0, "humidity": 55})
    assert response.status_code == 201

    # Test GET request
    response = client.get("/data")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
