from db import db

class SeatModel(db.Model):
    __tablename__ = "seats"

    id = db.Column(db.Integer, primary_key=True)
    is_booked = db.Column(db.Boolean, default=False)
    seat_number = db.Column(db.Integer, nullable=False)

    showtime_id = db.Column(db.Integer, db.ForeignKey("showtimes.id"), nullable=False)
    showtime = db.relationship("ShowtimeModel", back_populates="seats")

