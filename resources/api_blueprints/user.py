from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, verify_jwt_in_request, get_jwt
from blocklist import BLOCKLIST
from db import db

from schemas import UserSchema, InputTicketSchema, OutputTicketSchema
from models import UserModel, RoleModel, MovieModel, SeatModel, ShowtimeModel, TicketModel

from functools import wraps

blp = Blueprint("user", __name__, description="Operations on users", url_prefix="/user")


################################################################################################

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
################################################################################################


@blp.route("/refresh")
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

        role = RoleModel(name="regular")
        user.roles.append(role)

        db.session.add(user)
        db.session.commit()

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
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        return {"message": f"added admin role to user: {user.username}"}

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
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}


@blp.route("/account")
class UserAccount(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        user_id = get_jwt()["sub"]
        user = UserModel.query.get_or_404(user_id)
        return user


@blp.route("/delete/<int:user_id>")
class UserDelete(MethodView):
    @jwt_required(fresh=True)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "user deleted."}


@blp.route("/buy")
class UserBuy(MethodView):
    @jwt_required()
    @blp.arguments(InputTicketSchema)
    @blp.response(200, OutputTicketSchema)
    def post(self, buy_data):
        user = UserModel.query.get_or_404(get_jwt()["sub"])
        movie = MovieModel.query.get_or_404(buy_data["movie"])
        showtime = ShowtimeModel.query.get_or_404(buy_data["showtime"])
        seat = SeatModel.query.get_or_404(buy_data["seat"])
        ticket = TicketModel(movie=movie.movie_name, showtime=showtime.datetime, seat=seat.seat_number)

        if seat.is_booked:
            abort(500, message="Seat is already taken.")

        try:
            seat.is_booked = True
            user.tickets.append(ticket)
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return ticket


###########################################################################
# Testing route
@blp.route("/getall")
class UserGetAll(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users
###########################################################################