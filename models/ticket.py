from db import db

class TicketModel(db.Model):
    __tablename__ = "ticket"

    id = db.Column(db.Integer, primary_key=True)

    movie = db.Column(db.String, nullable=False)
    showtime = db.Column(db.DateTime, nullable=False)
    seat = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="tickets")
