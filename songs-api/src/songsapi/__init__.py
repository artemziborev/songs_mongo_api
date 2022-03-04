from flask import Flask
from flask_restx import Api, Resource
from flask_restx import reqparse
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .models import Song


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/yousician"
pymongo = PyMongo(app)
api = Api(app)

songs: Collection = pymongo.db.songs


parser = reqparse.RequestParser()


@api.route("/songs/")
@api.param("page")
class SongsList(Resource):
    @api.response(200, "Songs list")
    def get(self):

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


@api.route("/average_difficulty")
@api.param("level")
class SongsAverageDiffculty(Resource):
    def get(self):
        args = parser.parse_args()
        level = args.get('level', None)
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

        return [doc for doc in result]


@api.route("/search/")
class SongsSearch(Resource):
    def get(self):
        test_text = "Babysitting"
        cursor = songs.find(({"$text": {"$search": test_text}})) #the search is case insensitive by default
        return [Song(**doc).to_json() for doc in cursor]


@api.route("/add_rating/<string:song_id>/<int:rating>")
class AddSongRating(Resource):
    def post(self, song_id, rating:int):
        cursor = songs.find_one({"_id": song_id})



@api.route("/song_rating/<string:song_id>")
class SongRating(Resource):
    def get(self, song_id):
        cursor = songs.aggregate(
            [
                {"$match": {"level": song_id}},
                {"$group":
                     { "_id": "$rating",
                       "SumRating": { "$sum": "$rating" } }},
                {
                    "$group": {
                        "_id": "_id",
                        "AverageRating": {"$avg": "$SumRating"},
                        "HighestRating": {"$max": "$SumRating"},
                        "LowestRating": {"$min": "$SumRating"},
                    }
                },
            ]
        )
        return [doc for doc in cursor]

