from db import db

class SeatModel(db.Model):
    __tablename__ = "seats"

    id = db.Column(db.Integer, primary_key=True)

    seat_number = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("UserModel", back_populates="seats")

    showtime_id = db.Column(db.Integer, db.ForeignKey("showtimes.id"), nullable=False)
    showtime = db.relationship("ShowtimeModel", back_populates="seats")

