from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from resources.api_blueprints.user import role_required
from db import db

from schemas import GenreSchema
from models import GenreModel, MovieModel


blp = Blueprint("genre", __name__, description="Operations on genres", url_prefix="/genre")


@blp.route("/")
class GenreAdd(MethodView):
    @role_required("admin")
    @blp.arguments(GenreSchema)
    def post(self, genre_data):
        genre = GenreModel(**genre_data)
        try:
            db.session.add(genre)
            db.session.commit()
            return {"message": "Successfully created genre."}, 201
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/<int:genre_id>/<int:movie_id>")
class GenreMovieUnlink(MethodView):
    @role_required("admin")
    def post(self, genre_id, movie_id):
        genre = GenreModel.query.get_or_404(genre_id)
        movie = MovieModel.query.get_or_404(movie_id)
        genre.movies.append(movie)
        try:
            db.session.add(genre)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while committing changes to database.")
        return {"message": "Successfully linked genre and movie."}, 201

    @role_required("admin")
    def delete(self, genre_id, movie_id):
        genre = GenreModel.query.get_or_404(genre_id)
        movie = MovieModel.query.get_or_404(movie_id)
        genre.movie.remove(movie)
        try:
            db.session.add(genre)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while committing changes to database.")
        return {"message": "Successfully unlinked genre and movie."}, 200


@blp.route("/")
class Genre(MethodView):
    @blp.response(200, GenreSchema(many=True))
    def get(self):
        genres = GenreModel.query.all()
        return genres


@blp.route("/<int:genre_id>")
class Genre(MethodView):
    @role_required("admin")
    def delete(self, genre_id):
        genre = GenreModel.query.get_or_404(genre_id)
        try:
            genre.movies.clear()
            db.session.delete(genre)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Problem removing movie links from genre, deleting genre or committing database changes.")
        return {"message": "Successfully deleted genre."}, 200
