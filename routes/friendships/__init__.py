import flask
import flask_jwt_extended

from .request import friendship_request
from .accept import friendship_accept
from .remove import friendship_remove
from .list import friendship_list

friendships = flask.Blueprint("friendships", __name__)


@friendships.route("/request", methods=["POST"])
@flask_jwt_extended.jwt_required()
def request_friendship():
    user_id = flask_jwt_extended.get_jwt_identity()
    return friendship_request(user_id)


@friendships.route("/accept", methods=["PUT"])
@flask_jwt_extended.jwt_required()
def accept_friendship():
    user_id = flask_jwt_extended.get_jwt_identity()
    return friendship_accept(user_id)


@friendships.route("/remove", methods=["DELETE"])
@flask_jwt_extended.jwt_required()
def remove_friendship():
    user_id = flask_jwt_extended.get_jwt_identity()
    return friendship_remove(user_id)


@friendships.route("/list", methods=["GET"])
@flask_jwt_extended.jwt_required()
def list_friendships():
    user_id = flask_jwt_extended.get_jwt_identity()
    return friendship_list(user_id)
