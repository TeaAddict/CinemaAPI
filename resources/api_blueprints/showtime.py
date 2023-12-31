from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from resources.api_blueprints.user import role_required
from db import db

from schemas import ShowtimeSchema, PlainShowtimeSchema
from models import ShowtimeModel

blp = Blueprint("showtime", __name__, description="Operations on showtimes", url_prefix="/showtime")


@blp.route("/<int:movie_id>")
class ShowtimeAdd(MethodView):
    @role_required("admin")
    @blp.arguments(ShowtimeSchema)
    def post(self, showtime_data, movie_id):
        showtime = ShowtimeModel(**showtime_data, movie_id=movie_id)
        try:
            db.session.add(showtime)
            db.session.commit()
            return {"message": "Successfully added showtime to movie."}, 201
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/<int:showtime_id>")
class ShowtimeDelete(MethodView):
    @role_required("admin")
    def delete(self, showtime_id):
        try:
            showtime = ShowtimeModel.query.get(showtime_id)
            for seat in showtime.seats:
                db.session.delete(seat)
            db.session.delete(showtime)
            db.session.commit()
            return {"message": "Successfully deleted showtime."}, 200
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/<int:movie_id>")
class ShowtimeAdd(MethodView):
    @blp.response(200, PlainShowtimeSchema(many=True))
    def get(self, movie_id):
        showtime = ShowtimeModel.query.filter_by(movie_id=movie_id).all()
        return showtime


@blp.route("/")
class ShowtimeGet(MethodView):
    @blp.response(200, PlainShowtimeSchema(many=True))
    def get(self):
        showtimes = ShowtimeModel.query.all()
        return showtimes
