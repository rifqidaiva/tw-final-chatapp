import flask
import flask_jwt_extended

from .register import register
from .login import login
from .get_all import get_all_users
from .profile import (
    profile_get,
    profile_put,
    upload_profile_picture,
    serve_profile_picture,
)


users = flask.Blueprint("users", __name__)


@users.route("/register", methods=["POST"])
def register_route():
    return register()


@users.route("/login", methods=["POST"])
def login_route():
    return login()


@users.route("/get_all", methods=["GET"])
@flask_jwt_extended.jwt_required()
def get_all_users_route():
    user_id = flask_jwt_extended.get_jwt_identity()
    return get_all_users(user_id)


@users.route("/profile", methods=["GET", "PUT"])
@flask_jwt_extended.jwt_required()
def profile_route():
    user_id = flask_jwt_extended.get_jwt_identity()

    if flask.request.method == "GET":
        return profile_get(user_id)
    elif flask.request.method == "PUT":
        return profile_put(user_id)


@users.route("/profile/upload", methods=["POST"])
@flask_jwt_extended.jwt_required()
def upload_profile_picture_route():
    user_id = flask_jwt_extended.get_jwt_identity()
    return upload_profile_picture(user_id)


# serve profile picture
@users.route("/uploads/<user_id>/<filename>", methods=["GET"])
def serve_profile_picture(user_id: str, filename: str):
    return serve_profile_picture(user_id, filename)


__all__ = [
    "users",
]
