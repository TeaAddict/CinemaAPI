from marshmallow import Schema, fields


class PlainRoleSchema(Schema):
    name = fields.Str(dump_only=True)


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)


class PlainMovieSchema(Schema):
    id = fields.Int(dump_only=True)
    movie_name = fields.Str(required=True)
    description = fields.Str(required=True)


class PlainShowtimeSchema(Schema):
    id = fields.Int(dump_only=True)
    datetime = fields.DateTime(required=True)


class PlainSeatsSchema(Schema):
    id = fields.Int(dump_only=True)
    seat_number = fields.Int(required=True)
    is_booked = fields.Bool(dump_only=True)


class PlainGenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class InputTicketSchema(Schema):
    id = fields.Int(dump_only=True)
    movie = fields.Int(required=True)
    showtime = fields.Int(required=True)
    seat = fields.Int(required=True)


class OutputTicketSchema(Schema):
    id = fields.Int(dump_only=True)
    movie = fields.Str(required=True)
    showtime = fields.DateTime(required=True)
    seat = fields.Int(required=True)


class RoleSchema(PlainRoleSchema):
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class UserSchema(PlainUserSchema):
    roles = fields.List(fields.Nested(PlainRoleSchema()), dump_only=True)
    tickets = fields.List(fields.Nested(OutputTicketSchema()), dump_only=True)


class ShowtimeSchema(PlainShowtimeSchema):
    movie = fields.Nested(PlainMovieSchema(), dump_only=True)
    seats = fields.List(fields.Nested(PlainSeatsSchema()), dump_only=True)


class MovieShowtimeSchema(PlainShowtimeSchema):
    seats = fields.List(fields.Nested(PlainSeatsSchema()), dump_only=True)


class SeatSchema(PlainSeatsSchema):
    showtime = fields.Nested(PlainShowtimeSchema(), dump_only=True)


class GenreSchema(PlainGenreSchema):
    movies = fields.List(fields.Nested(PlainMovieSchema()), dump_only=True)


class MovieSchema(PlainMovieSchema):
    showtimes = fields.List(fields.Nested(MovieShowtimeSchema), dump_only=True)


class MovieGenreSchema(PlainMovieSchema):
    genres = fields.List(fields.Nested(PlainGenreSchema), dump_only=True)
