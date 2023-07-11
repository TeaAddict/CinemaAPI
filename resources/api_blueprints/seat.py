from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from resources.api_blueprints.user import role_required
from db import db

from schemas import PlainSeatsSchema
from models import SeatModel


blp = Blueprint("seat", __name__, description="Operations on seat", url_prefix="/seat")


@blp.route("/<int:seat_num>/<int:showtime_id>")
class SeatAdd(MethodView):
    @role_required("admin")
    def post(self, seat_num, showtime_id):
        try:
            for i in range(1, int(seat_num)):
                seat = SeatModel(seat_number=i, showtime_id=showtime_id)
                db.session.add(seat)
            db.session.commit()
            return {"message": "Seats successfully added."}, 201
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/<int:showtime_id>")
class SeatDelete(MethodView):
    @role_required("admin")
    def delete(self, showtime_id):
        try:
            selected_rows = SeatModel.query.filter_by(showtime_id=showtime_id).all()
            for row in selected_rows:
                db.session.delete(row)
            db.session.commit()
            return {"message": "Seats successfully deleted."}, 200
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/<int:showtime_id>")
class SeatGet(MethodView):
    @blp.response(200, PlainSeatsSchema(many=True))
    def get(self, showtime_id):
        seats = SeatModel.query.filter_by(showtime_id=showtime_id).all()
        return seats
