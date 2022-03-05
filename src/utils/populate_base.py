from pymongo import MongoClient
import json
from pathlib import Path
import os


BASE_DIR = Path(__file__).parent.parent.parent

MONGO_DB_HOST = os.getenv('MONGO_DB_HOST')
MONGO_DB_DATABASE_NAME = os.getenv('MONGO_DB_DATABASE_NAME')

client = MongoClient(f"mongodb://{MONGO_DB_HOST}:27017")
SONGS_DATA_FILE_PATH = os.path.join(BASE_DIR, 'data', 'songs.json')
db = client.yousician
songs = db.songs

def populate_db():
    with open(SONGS_DATA_FILE_PATH) as file:
        id_counter = 0
        lines = file.readlines()
        for line in lines:
            data = json.loads(line.strip())
            data["song_id"] = id_counter # we add this field for search by "song_id" field
            songs.insert_one(data)
            id_counter +=1


def create_indexes():
    songs.drop_indexes()
    songs.create_index([('artist', 'text'), ('title', 'text')],
                       name='song_search')



if __name__ == '__main__':
    populate_db()
    create_indexes()
