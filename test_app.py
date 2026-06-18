import pytest
import sqlite3
import app

@pytest.fixture
def client():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    app.get_db = lambda: conn
    app.init_db()

    with app.app.test_client() as client:
        yield client

    conn.close()

def test_home_loads(client):
    res = client.get("/")
    assert res.status_code == 200

def test_submit_entry(client):
    client.post("/submit", data={"name": "test_user", "message": "Hello!"})
    res = client.get("/")
    assert b"test_user" in res.data
    assert b"Hello!" in res.data

def test_empty_submit_ignored(client):
    client.post("/submit", data={"name": "", "message": ""})
    res = client.get("/")
    assert b"No entries yet" in res.data