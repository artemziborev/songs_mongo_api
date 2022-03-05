import pytest
import json
from src.songsapi import app, songs


@pytest.fixture()
def client():
    return app.test_client()



def test_songs_list_status_code(client):
    response = client.get("/songs/")
    assert response.status_code == 200


def test_songs_list_rsponse_content(client):
    response = client.get("/songs/")
    assert response.content_type == "application/json"


def test_average_difficulty_status_code(client):
    response = client.get("/average_difficulty/?level=3")
    assert response.status_code == 200


def test_average_difficulty_error_status_code(client):
    response = client.get("/average_difficulty/?level=1")
    message = {"message": "No songs with matching level found"}
    assert response.status_code == 400
    assert message == response.json


def test_average_difficulty_response_content(client):
    response = client.get("/songs/")
    assert response.content_type == "application/json"


def test_average_difficulty_logic(client):
    response = client.get("/average_difficulty/?level=3")
    expected = [{"_id": "_id", "AverageDifficulty": 2}]
    assert response.json == expected


def test_search_status_code(client):
    response = client.get("/search/Babysitting")
    assert response.status_code == 200


def test_search_content_type(client):
    response = client.get("/search/Babysitting")
    assert response.content_type == "application/json"


def test_search_logic(client):
    data = {
        "artist": "The Yousicians",
        "title": "Lazy Song",
        "difficulty": 7,
        "level": 6,
        "released": "2016-07-01",
        "song_id": 100,
    }
    songs.insert_one(data)
    expected = "Lazy Song"
    response = client.get("/search/Lazy Song")
    assert response.json[0]["title"] == expected
    songs.delete_one({"song_id": 100})

def test_add_rating_status_code_and_response_type(client):
    data = {"song_id": 3, "rating": 5}
    response = client.post("/add_rating/",
                           data=json.dumps(data),
                           content_type='application/json'
                           )
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_add_rating_wrong_rating_level(client):
    data = {"song_id": 3, "rating": 6}
    response = client.post("/add_rating/",
                           data=json.dumps(data),
                           content_type='application/json'
                           )
    message = {"message": "Rating must be between 1 and 5"}
    assert response.status_code == 400
    assert response.json == message


def test_add_rating_logic(client):
    song_data = {
        "artist": "The Yousicians",
        "title": "Super Song",
        "difficulty": 7,
        "level": 6,
        "released": "2016-07-01",
        "song_id": 1000,
    }
    songs.insert_one(song_data)
    data = {"song_id": 1000, "rating": 5}
    response = client.post("/add_rating/",
                           data=json.dumps(data),
                           content_type='application/json'
                           )
    assert response.json['rating'] == {"5": 1}
    songs.delete_one({"song_id": 1000})
