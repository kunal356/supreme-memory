from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_compute_happy_path():
    payload = {
        "traversals": [{"nodes": [{"id": 0}, {"id": 1}, {"id": 2}]}],
        "pathCosts": [{"node_id": 1, "cost": 5}, {"node_id": 2, "cost": 7}, {"node_id": 1, "cost": 3}],
    }
    r = client.post("/compute", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body[0]["total_cost"] == 15


def test_compute_validation_unknown_node():
    payload = {
        "traversals": [{"nodes": [{"id": 0}, {"id": 1}]}],
        "pathCosts": [{"node_id": 5, "cost": 10}],
    }
    r = client.post("/compute", json=payload)
    assert r.status_code == 400
