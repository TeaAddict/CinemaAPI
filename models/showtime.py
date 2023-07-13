
from db import db

class ShowtimeModel(db.Model):
    __tablename__ = "showtimes"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)

    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    movie = db.relationship("MovieModel", back_populates="showtimes")

    seats = db.relationship("SeatModel", cascade="all, delete", back_populates="showtime")
