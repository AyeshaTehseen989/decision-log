def make_payload(**overrides):
    payload = {
        "title": "Use SQLite",
        "context": "We need a simple database for a small app.",
        "decision": "Use SQLite through Python's built-in module.",
    }
    payload.update(overrides)
    return payload


def test_status_can_change_to_accepted(client):
    client.post("/decisions", json=make_payload())
    response = client.patch("/decisions/1/status", json={"status": "accepted"})
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"


def test_status_cannot_be_set_to_superseded_by_hand(client):
    client.post("/decisions", json=make_payload())
    response = client.patch("/decisions/1/status", json={"status": "superseded"})
    assert response.status_code == 422


def test_supersede_creates_new_and_marks_old(client):
    client.post("/decisions", json=make_payload())
    response = client.post(
        "/decisions/1/supersede", json=make_payload(title="Use Postgres")
    )
    assert response.status_code == 201
    assert response.json()["id"] == 2
    assert response.json()["status"] == "accepted"

    old = client.get("/decisions/1").json()
    assert old["status"] == "superseded"
    assert old["superseded_by"] == 2


def test_supersede_missing_decision_returns_404(client):
    response = client.post("/decisions/999/supersede", json=make_payload())
    assert response.status_code == 404


def test_cannot_supersede_twice(client):
    client.post("/decisions", json=make_payload())
    client.post("/decisions/1/supersede", json=make_payload(title="Second"))
    response = client.post("/decisions/1/supersede", json=make_payload(title="Third"))
    assert response.status_code == 409


def test_superseded_decision_cannot_change_status(client):
    client.post("/decisions", json=make_payload())
    client.post("/decisions/1/supersede", json=make_payload(title="Second"))
    response = client.patch("/decisions/1/status", json={"status": "accepted"})
    assert response.status_code == 409