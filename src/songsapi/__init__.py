from flask import Flask, request
from werkzeug.exceptions import BadRequest
from flask_restx import Api, Resource, fields
from flask_restx import reqparse
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .models import Song
import os

MONGO_DB_HOST = os.getenv('MONGO_DB_HOST')
MONGO_DB_DATABASE_NAME = os.getenv('MONGO_DB_DATABASE_NAME')
app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{MONGO_DB_HOST}:27017/{MONGO_DB_DATABASE_NAME}"
pymongo = PyMongo(app)
api = Api(app, description='Songs Api')

songs: Collection = pymongo.db.songs


parser = reqparse.RequestParser()


@api.route("/songs/")
@api.param("page")
class SongsList(Resource):
    @api.response(200, "Songs list")
    def get(self):

        parser.add_argument("page", type=int, location="args")
        args = parser.parse_args()
        page = args.get("page", None)
        per_page = 3

        if page is not None:
            cursor = (
                songs.find().sort("artist").skip(per_page * (page - 1)).limit(per_page)
            )
        else:
            cursor = songs.find()
        return [Song(**doc).to_json() for doc in cursor]


@api.route("/average_difficulty/")
@api.param("level")
class SongsAverageDiffculty(Resource):
    def get(self):
        parser.add_argument("level", type=int, location="args")
        args = parser.parse_args()
        level = args.get("level", None)
        if level is not None:
            result = songs.aggregate(
                [
                    {"$match": {"level": level}},
                    {
                        "$group": {
                            "_id": "_id",
                            "AverageDifficulty": {"$avg": "$difficulty"},
                        }
                    },
                ]
            )
        else:
            result = [
                {
                    "$group": {
                        "_id": "_id",
                        "AverageDifficulty": {"$avg": "$difficulty"},
                    }
                }
            ]

        result_list = [doc for doc in result]

        if len(list(result_list)) == 0:
            raise BadRequest("No songs with matching level found")
        else:
            return result_list



@api.route("/search/<string:message>")
class SongsSearch(Resource):
    def get(self, message):
        cursor = songs.find(
            ({"$text": {"$search": message}})
        )  # the search is case-insensitive by default
        return [Song(**doc).to_json() for doc in cursor]


add_rating_fields = api.model(
    "rating_fileds",
    {
        "song_id": fields.Integer(required=True, description="Song Id"),
        "rating": fields.Integer(required=True, description="Rating"),
    },
)


@api.route("/add_rating/")
class AddSongRating(Resource):
    @api.expect(add_rating_fields)
    def post(self):
        data = request.json
        cursor = songs.find_one({"song_id": data["song_id"]})
        song = Song(**cursor).to_json()
        current_rating = song.get("rating", None)
        if int(data["rating"]) < 1 or int(data["rating"] > 5):
            raise BadRequest("Rating must be between 1 and 5")

        if current_rating is None:
            songs.update_one(
                {"song_id": data["song_id"]},
                {"$set": {"rating": {str(data["rating"]): 1}}},
            )
        else:
            rating_group = str(data["rating"])
            songs.update_one(
                {"song_id": data["song_id"]}, {"$inc": {f"rating.{rating_group}": 1}}
            )

        cursor = songs.find_one({"song_id": data["song_id"]})

        return Song(**cursor).to_json()


@api.route("/song_rating/<int:song_id>")
class SongRating(Resource):
    def get(self, song_id):
        cursor = songs.aggregate(
            [
                {"$match": {"song_id": song_id}},
                {"$group": {"_id": {"rating":"$rating"}}},
                #TODO fix somehow min, max and average agregations
                # {
                #     "$group": {
                #         "_id": "_id",
                #         "AverageRating": {"$avg": "$rating"},
                #         "HighestRating": {"$max": "$rating"},
                #         "LowestRating": {"$min": "$rating"},
                #     }
                # },
            ]
        )
        return [doc for doc in cursor]
