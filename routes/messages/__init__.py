import flask
import flask_jwt_extended

from .get import messages_get

messages = flask.Blueprint("messages", __name__)


@messages.route("/get", methods=["GET"])
@flask_jwt_extended.jwt_required()
def get_messages():
    user_id = flask_jwt_extended.get_jwt_identity()
    return messages_get(user_id)
