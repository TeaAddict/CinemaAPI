from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from models import MovieModel
from schemas import MovieSchema, PlainMovieSchema, MovieGenreSchema
from resources.api_blueprints.user import role_required

blp = Blueprint("movie", __name__, description="Operations on movies", url_prefix="/movie")

@blp.route("/create")
class MovieCreate(MethodView):

    @role_required("admin")
    @blp.arguments(MovieSchema)
    def post(self, movie_data):
        movie = MovieModel(movie_name=movie_data["movie_name"], description=movie_data["description"])
        try:
            db.session.add(movie)
            db.session.commit()
            return {"message": f"Successfully created movie: {movie_data['movie_name']}"}
        except SQLAlchemyError as e:
            abort(500, message=str(e))

@blp.route("/delete/<int:movie_id>")
class MovieCreate(MethodView):
    @role_required("admin")
    def delete(self, movie_id):
        movie = MovieModel().query.get_or_404(movie_id)
        if not movie.showtimes:
            db.session.delete(movie)
            db.session.commit()
            return {"message": f"Successfully deleted movie"}
        abort(400, message="Error deleting movie.")


@blp.route("/get/<movie_id>")
class MovieGet(MethodView):
    @blp.response(200, MovieSchema())
    def get(self, movie_id):
        movie = MovieModel.query.get_or_404(movie_id)
        return movie


@blp.route("/get")
class MovieGet(MethodView):
    @blp.response(200, MovieGenreSchema(many=True))
    def get(self):
        movies = MovieModel.query.all()
        return movies


@blp.route("/get/all")
class MovieGet(MethodView):
    @blp.response(200, MovieSchema(many=True))
    def get(self):
        movies = MovieModel.query.all()
        return movies

