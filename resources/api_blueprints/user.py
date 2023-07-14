from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, verify_jwt_in_request, get_jwt
from blocklist import BLOCKLIST
from functools import wraps
from db import db

from schemas import UserSchema, UserAccountSchema
from models import UserModel, RoleModel, SeatModel, ShowtimeModel, MovieModel

blp = Blueprint("user", __name__, description="Operations on users", url_prefix="/user")


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # Verify JWT token in the request
            subject_id = get_jwt()["sub"]  # Get the subject ID from the JWT token
            user = UserModel.query.get(subject_id)  # Retrieve the user based on the subject ID
            role_names = [role_obj.name for role_obj in user.roles]  # lst of RoleModel obj to lst of str(roles)
            if user is None or role not in role_names:
                return {'message': f'Insufficient privileges.'}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


@blp.route("/refresh-token")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt()["sub"]
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="User with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        role = RoleModel.query.filter(RoleModel.name == "regular").first()
        if not role:
            role = RoleModel(name="regular")

        user.roles.append(role)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {
                "access_token": access_token,
                "refresh_token": refresh_token
                }, 201


@blp.route("/admin/<int:user_id>")
class AdminUserId(MethodView):
    @role_required("admin")
    @jwt_required()
    def post(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        role = RoleModel(name="admin")
        try:
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": f"added admin role to user: {user.username}"}, 201

    @role_required("admin")
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 201
        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}, 201


@blp.route("/account")
class UserAccount(MethodView):
    @jwt_required()
    @blp.response(200, UserAccountSchema)
    def get(self):
        user_id = get_jwt()["sub"]
        user = UserModel.query.get_or_404(user_id)
        user_movies = []
        for seat in user.seats:
            showtime = ShowtimeModel.query.get_or_404(seat.showtime_id)
            movie = MovieModel.query.get_or_404(showtime.movie_id)
            user_movies.append({"movie": movie.movie_name,
                                "showtime": showtime.datetime,
                                "seat_number": seat.seat_number})
        user_data = {"username": user.username, "password": user.password, "movies": user_movies}
        return user_data


@blp.route("/<int:user_id>")
class UserDelete(MethodView):
    @jwt_required(fresh=True)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "user deleted."}, 200


@blp.route("/buy/<int:seat_id>")
class UserBuy(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def post(self, seat_id):
        user = UserModel.query.get_or_404(get_jwt()["sub"])
        seat = SeatModel.query.get_or_404(seat_id)

        if seat.user_id:
            abort(500, message="Seat is already taken.")

        try:
            seat.user_id = get_jwt()["sub"]
            user.seats.append(seat)
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return user


@blp.route("/all")
class UserGetAll(MethodView):
    @role_required("admin")
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users

