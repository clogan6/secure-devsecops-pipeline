from app.app import app

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

# Validating our greet response
def test_greet_valid_username():
    client = app.test_client()
    response = client.get("/greet?user=Caleb")

    assert response.status_code == 200
    assert response.json["message"] == "Hello, Caleb!"


def test_greet_missing_username():
    client = app.test_client()
    response = client.get("/greet")

    assert response.status_code == 400


def test_greet_empty_username():
    client = app.test_client()
    response = client.get("/greet?user=")

    assert response.status_code == 400


def test_greet_invalid_characters():
    client = app.test_client()
    response = client.get("/greet?user=Caleb!")

    assert response.status_code == 400


def test_greet_username_too_long():
    client = app.test_client()
    username = "A" * 51
    response = client.get("/greet", query_string={"user": username})

    assert response.status_code == 400


def test_greet_whitespace_normalization():
    client = app.test_client()
    response = client.get("/greet", query_string={"user": " Caleb "})

    assert response.status_code == 200
    assert response.json["message"] == "Hello, Caleb!"

# Testing for security headers
def test_security_headers_on_successful_response():
    client = app.test_client()
    response = client.get("/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Cache-Control"] == "no-store"


def test_security_headers_on_error_response():
    client = app.test_client()
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Cache-Control"] == "no-store"