import flask
import flask_jwt_extended

from .register import register
from .login import login
from .profile import profile_get, profile_put, upload_profile_picture

import utils

users = flask.Blueprint("users", __name__)


@users.route("/register", methods=["POST"])
def register_route():
    return register()


@users.route("/login", methods=["POST"])
def login_route():
    return login()


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
    user = utils.User.from_id(user_id)
    if user is None:
        return utils.Response(
            status_code=404,
            msg="User not found",
        ).send()

    return flask.send_from_directory(
        f"uploads/{user_id}", filename, as_attachment=False
    )


__all__ = [
    "users",
]
