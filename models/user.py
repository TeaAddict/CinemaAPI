from db import db

class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    roles = db.relationship("RoleModel", back_populates="users", secondary="users_roles")

    tickets = db.relationship("TicketModel", back_populates="user")
