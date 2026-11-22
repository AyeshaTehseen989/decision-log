def make_payload(**overrides):
    payload = {
        "title": "Use SQLite",
        "context": "We need a simple database for a small app.",
        "decision": "Use SQLite through Python's built-in module.",
    }
    payload.update(overrides)
    return payload


def test_create_decision_returns_201_and_saved_data(client):
    response = client.post("/decisions", json=make_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Use SQLite"
    assert body["status"] == "proposed"


def test_list_decisions_returns_newest_first(client):
    client.post("/decisions", json=make_payload(title="First"))
    client.post("/decisions", json=make_payload(title="Second"))
    response = client.get("/decisions")
    assert response.status_code == 200
    titles = [item["title"] for item in response.json()]
    assert titles == ["Second", "First"]


def test_get_missing_decision_returns_404(client):
    response = client.get("/decisions/999")
    assert response.status_code == 404


def test_create_rejects_empty_title(client):
    response = client.post("/decisions", json=make_payload(title=""))
    assert response.status_code == 422