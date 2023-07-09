from db import db

class MovieTagModel(db.Model):
    __tablename__ = "movie_genre"

    id = db.Column(db.Integer, primary_key=True)

    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
