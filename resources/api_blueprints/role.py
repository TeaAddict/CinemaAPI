from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from resources.api_blueprints.user import role_required
from db import db

from schemas import RoleSchema
from models import RoleModel

blp = Blueprint("role", __name__, description="Operations on role", url_prefix="/role")


@blp.route("/")
class Role(MethodView):
    @role_required("admin")
    @blp.arguments(RoleSchema)
    def post(self, role_data):
        role = RoleModel(**role_data)
        try:
            db.session.add(role)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "Successfully created role."}

    @role_required("admin")
    @blp.response(200, RoleSchema(many=True))
    def get(self):
        role = RoleModel.query.all()
        return role

