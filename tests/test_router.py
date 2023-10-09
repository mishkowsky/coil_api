from pytest_postgresql import factories
from fastapi.testclient import TestClient
from src.router import app

test_db = factories.postgresql_proc(port=None, dbname="test_db")


def test_post_coil(create_test_data):
    client = TestClient(app)

    response = client.post('/coil', json={'length': 23, 'weight': 12})
    assert response.status_code == 200
    assert response.json() == 6

    response = client.post('/coil', json={'length': -1, 'weight': 1})
    assert response.status_code == 422

    response = client.post('/coil', json={'weight': 1})
    assert response.status_code == 422


def test_delete_coil(create_test_data):
    client = TestClient(app)

    response = client.request('DELETE', '/coil', json={'id': 4})
    assert response.status_code == 204

    response = client.request('DELETE', '/coil', json={'id': 4})
    assert response.status_code == 204

    response = client.request('DELETE', '/coil', json={'id': 100})
    assert response.status_code == 404


def test_get_coils(create_test_data):
    client = TestClient(app)

    response = client.request('GET', '/coil', json={
        "id_range": {"start": 1, "end": 10},
        "length_range": {"start": 12, "end": 25}
    })
    assert response.status_code == 200
    assert len(response.json()) == 3
