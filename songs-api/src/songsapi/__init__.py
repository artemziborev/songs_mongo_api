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
        page = args.get('page', None)
        per_page = 3

        if page is not None:
            cursor = songs.find().sort("artist").skip(per_page *(page -1)).limit(per_page)
        else:
            cursor = songs.find()
        return [Song(**doc).to_json() for doc in cursor]


@api.route("/average_difficulty")
@api.param('level')
class SongsAverageDiffculty(Resource):
    def get(self):
        args = parser.parse_args()
        level = args.get('level', None)
        pass


@api.route("/search/<string:message>")
class SongsSearch(Resource):
    def get(self):
        pass


@api.route("/add_rating/<string:song_id>/<int:rating>")
class AddSongRating(Resource):
    def post(self):
        pass


@api.route("/song_rating/<string:song_id>")
class SongRating(Resource):
    def get(self):
        pass



