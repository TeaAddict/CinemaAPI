from db import db

class GenreModel(db.Model):
    __tablename__ = "genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    movies = db.relationship("MovieModel", back_populates="genres", secondary="movie_genre")
