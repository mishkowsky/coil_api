from datetime import datetime
from fastapi.testclient import TestClient
from src.router import app
from tests.utils import count_stats_for_test_data

client = TestClient(app)


def test_post_coil(db_session):

    response = client.post('/coil', json={'length': 23, 'weight': 12})
    assert response.status_code == 200
    assert response.json() == 1

    response = client.post('/coil', json={'length': -1, 'weight': 1})
    assert response.status_code == 422

    response = client.post('/coil', json={'weight': 1})
    assert response.status_code == 422


def test_delete_coil(create_test_data):

    response = client.request('DELETE', '/coil', json={'id': 1})
    assert response.status_code == 204

    response = client.request('DELETE', '/coil', json={'id': 1})
    assert response.status_code == 204

    response = client.request('DELETE', '/coil', json={'id': 100})
    assert response.status_code == 404


def test_get_coils(create_test_data):

    response = client.request('GET', '/coil', json={
        "id_range": {
            "start": 1,
            "end": 5
        },
        "length_range": {
            "start": 12,
            "end": 25
        }
    })
    expected = len(list(filter(lambda coil: 1 <= coil.id <= 5 and 12 <= coil.length <= 25, create_test_data)))
    assert response.status_code == 200
    assert len(response.json()) == expected

    response = client.request('GET', '/coil', json={
        "id_range": {
            "start": 6,
            "end": 5
        }
    })
    assert response.status_code == 422

    response = client.request('GET', '/coil', json={})
    assert response.status_code == 422


def test_get_stats(create_test_data):

    date_format = '%Y-%m-%dT%H:%M:%S.%f'
    start_date_str = '2023-10-06T01:16:00.850625'
    end_date_str = '2023-10-08T01:16:00.850625'

    start_date = datetime.strptime(start_date_str, date_format)
    end_date = datetime.strptime(end_date_str, date_format)

    response = client.request('GET', '/coil/stats', json={
        "start": start_date_str,
        "end": end_date_str
    }).json()

    expected = count_stats_for_test_data(create_test_data, start_date, end_date).model_dump(mode='json')

    assert response == expected

    response = client.request('GET', '/coil/stats', json={})

    assert response.status_code == 422


def test_database_unavailable():
    response = client.request('DELETE', '/coil', json={'id': 1})
    assert response.status_code == 500
