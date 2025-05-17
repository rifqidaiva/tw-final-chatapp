import flask
import flask_jwt_extended

from .register import register
from .login import login
from .profile import profile_get, profile_put

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


__all__ = [
    "users",
]
