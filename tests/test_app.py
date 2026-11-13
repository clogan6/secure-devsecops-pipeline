#from app.app import app

def test_health_endpoint():
    # Create Flask's test client
    client = app.test_client()

    # Send a GET request to the health endpoint
    response = client.get("/health")

    # Verify the response
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_unknown_endpoint():
    client = app.test_client()

    # Request an endpoint that does not exist
    response = client.get("/does-not-exist")

    # Verify Flask returns a 404
    assert response.status_code == 404


def test_wrong_http_method():
    client = app.test_client()

    # Attempt to POST to an endpoint that only accepts GET
    response = client.post("/health")

    # Verify Flask rejects the request
    assert response.status_code == 405
