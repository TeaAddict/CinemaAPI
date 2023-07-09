from db import db


class UserRolesModel(db.Model):
    __tablename__ = "users_roles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
