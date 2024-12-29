"""Test app genenal pages."""


def test_index_page(client):
    """Test index page."""

    with client as c:
        response = c.get("/")
        assert response.status_code == 200
        assert b"This is the SJD Babylab database" in response.data


def test_index_page_token(client, app):
    """Test index page."""
    response = client.post("/", data={"apiToken": app.config["API_KEY"], "email": ""})
    assert response.status_code == 200
    assert b"This is the SJD Babylab database" in response.data
    assert b"Incorrect token" not in response.data

    response = client.post("/", data={"apiToken": "badtoken", "email": ""})
    assert response.status_code == 200
    assert b"Incorrect token" in response.data


def test_dashboard_page(client):
    """Test index page."""
    response = client.get("/dashboard")
    assert response.status_code == 200


def test_studies(client):
    """Test studies endpoint."""
    response = client.get("/studies")
    assert response.status_code == 200


def test_studies_input(client):
    """Test studies endpoint with input."""

    response = client.post("/studies", data={"inputStudy": "1"})
    assert response.status_code == 200

    response = client.post("/studies", data={"inputStudy": "2"})
    assert response.status_code == 200

    response = client.post("/studies", data={"inputStudy": "3"})
    assert response.status_code == 200


def test_other(client):
    """Test studies endpoint."""
    response = client.get("/other")
    assert response.status_code == 200


def test_other_backup(client):
    """Test studies endpoint."""
    response = client.post("/other")
    assert response.status_code == 200
