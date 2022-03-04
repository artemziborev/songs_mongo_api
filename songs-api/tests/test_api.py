import pytest
from src.songsapi import app

@pytest.fixture()
def client():
    return app.test_client()

def test_songs_list_status_code(client):
    response = client.get('/songs/')
    assert response.status_code == 200

