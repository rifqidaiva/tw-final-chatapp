import flask
from .register import register

users = flask.Blueprint("users", __name__)


# MARK: /users/register
@users.route("/register", methods=["POST"])
def register_route():
    return register()


__all__ = [
    "users",
]
