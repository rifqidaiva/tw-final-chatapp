import flask
import flask_socketio
import flask_jwt_extended

import utils
import utils.message

socketio = flask_socketio.SocketIO(async_mode="eventlet")


# MARK:  connect
@socketio.on("connect")
def connect():
    """
    Handle a new connection to the WebSocket.
    """
    # Get token from the request
    auth_header = flask.request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        utils.log(message="Authorization header missing or invalid")
        return False

    access_token = auth_header.split(" ")[1]

    # Verify the token
    try:
        decoded_token = flask_jwt_extended.decode_token(access_token)
        user_id = decoded_token["sub"]
        if user_id is None:
            utils.log(message="User ID not found in token")
            return False

        # Store the user ID
        flask_socketio.join_room(user_id)
        flask.session["user_id"] = user_id
        utils.log(message=f"User {user_id} connected")

    except Exception as e:
        utils.log(message=f"Token verification failed: {str(e)}")
        return False

    return True


# MARK:  disconnect
@socketio.on("disconnect")
def disconnect():
    """
    Handle a disconnection from the WebSocket.
    """
    user_id = flask.session.get("user_id")
    if user_id:
        utils.log(message=f"User {user_id} disconnected")
        del flask.session["user_id"]
        flask_socketio.leave_room(user_id)
    else:
        utils.log(message="User ID not found in session")


# MARK:  message
@socketio.on("message")
def handle_message(data):
    """
    Handle incoming messages.
    """
    user_id = flask.session.get("user_id")
    if not user_id:
        utils.log(message="User ID not found in session")
        return False

    utils.log(message=f"Received message from {user_id}: {data}")

    message = utils.message.Message(
        id=data.get("id"),
        sender_id=user_id,
        receiver_id=data.get("receiver_id"),
        content=data.get("content"),
        file_path=data.get("file_path"),
        file_name=data.get("file_name"),
        file_type=data.get("file_type"),
        timestamp=data.get("timestamp"),
    )

    # Validate the message
    if not message.content and not message.file_path:
        utils.log(message="Message content and file path are both empty")
        return False

    if not message.validate():
        utils.log(message="Message validation failed")
        return False

    # Save the message to the database
    message.sender_id = user_id
    message.save()

    # Emit the message to the receiver
    receiver_id = message.receiver_id
    if receiver_id:
        socketio.emit("message", message.to_dict(), to=receiver_id)
        utils.log(message=f"Message sent to {receiver_id}: {message.to_dict()}")
    else:
        utils.log(message="Receiver ID not found in message data")


# MARK: upload
@socketio.on("upload")
def handle_upload(data):
    """
    Handle file uploads.
    """
    user_id = flask.session.get("user_id")
    if not user_id:
        utils.log(message="User ID not found in session")
        return False

    utils.log(message=f"Received upload from {user_id}: {data}")

    # Check for file and receiver_id
    file = data.get("file")
    receiver_id = data.get("receiver_id")
    if not file:
        utils.log(message="File is empty or not provided")
        return False
    if not receiver_id:
        utils.log(message="Receiver ID not found in upload data")
        return False

    # Create a message entry in the database (without file_path yet)
    message = utils.message.Message(
        sender_id=user_id,
        receiver_id=receiver_id,
        content=data.get("content", ""),
        file_path="",  # will be updated after saving file
        file_name=file.filename,
        file_type=file.content_type,
        timestamp=data.get("timestamp"),
    )
    message.save()  # Save to get the message.id

    # Save the file using message.id
    upload_dir = f"uploads/{user_id}"
    utils.ensure_dir(upload_dir)
    file_path = f"{upload_dir}/{message.id}_{file.filename}"
    file.save(file_path)

    # Update message with file_path and save again
    message.file_path = file_path
    message.save()

    # Emit the message from database
    socketio.emit("message", message.to_dict(), to=receiver_id)
    utils.log(
        message=f"File uploaded and message sent to {receiver_id}: {message.to_dict()}"
    )


# MARK: delete_message
@socketio.on("delete_message")
def handle_delete_message(data):
    """
    menghapus pesan atau file yang dikirim
    """
    user_id = flask.session.get("user_id")
    if not user_id:
        utils.log(message="User ID not found in session")
        return False

    message_id = data.get("message_id")
    if not message_id:
        utils.log(message="Message ID not found in delete data")
        return False

    # Delete the message from the database
    message = utils.message.Message.from_id(message_id)
    if message and (message.sender_id == user_id or message.receiver_id == user_id):
        message.delete()
        utils.log(message=f"Message {message_id} deleted by {user_id}")
        socketio.emit(
            "delete_message", {"message_id": message_id}, to=message.receiver_id
        )
    else:
        utils.log(message="Message not found or permission denied")
