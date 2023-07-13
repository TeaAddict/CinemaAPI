from db import db

class MovieModel(db.Model):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(90), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    showtimes = db.relationship("ShowtimeModel", cascade="all, delete", back_populates="movie")

    genres = db.relationship("GenreModel", back_populates="movies", secondary="movie_genre")


