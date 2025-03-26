from flask import request
from flask_socketio import SocketIO
from flask_jwt_extended import decode_token

import messages

socketio = SocketIO(async_mode="eventlet")
users = {}


@socketio.on("connect")
def connect():
    # Get token from header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        print("\033[96m" + "Authorization header is missing or invalid" + "\033[0m")
        return False

    access_token = auth_header.split(" ")[1]

    try:
        decoded_token = decode_token(access_token)
        user_id = decoded_token.get("sub")
        if user_id is None:
            print("\033[96m" + "User ID is None" + "\033[0m")
            return False

        # Store the user ID and socket ID
        users[request.sid] = user_id
        print("\033[96m" + "Connect: ", request.sid + ": " + str(user_id) + "\033[0m")
    except Exception as e:
        print("\033[96m" + f"Token decoding failed: {str(e)}" + "\033[0m")
        return False

    print("\033[96m" + "Users: ", users, "\033[0m")


@socketio.on("disconnect")
def disconnect():
    # Remove the user ID and socket ID mapping
    user_id = users.pop(request.sid, None)
    if user_id is None:
        print("\033[96m" + "User ID is None" + "\033[0m")
        return False

    print("\033[96m" + "Disconnect: ", request.sid + ": " + str(user_id) + "\033[0m")
    print("\033[96m" + "Users: ", users, "\033[0m")


@socketio.on("message")
def message(data):
    sender_id = users.get(request.sid)
    if sender_id is None:
        print("\033[96m" + "Sender ID is None" + "\033[0m")
        return False

    # Validate that only one of receiver_id or group_id is provided
    receiver_id = data.get("receiver_id")
    group_id = data.get("group_id")
    if (receiver_id is not None and group_id is not None) or (
        receiver_id is None and group_id is None
    ):
        print(
            "\033[96m"
            + "Invalid data: Provide either receiver_id or group_id, but not both"
            + "\033[0m"
        )
        return False

    if receiver_id is not None:
        # Handle sending to a specific user
        if not messages.send_message(sender_id, receiver_id, data["content"]):
            print("\033[96m" + "Message sending to user failed" + "\033[0m")
            return False

        data["sender_id"] = sender_id

        # Send the message to the receiver
        receiver_sid = [sid for sid, user_id in users.items() if user_id == receiver_id]
        if not receiver_sid:
            print("\033[96m" + "Receiver is not connected" + "\033[0m")
            return False
        for sid in receiver_sid:
            socketio.emit("message", data, room=sid)

    elif group_id is not None:
        # Handle sending to a group
        if not messages.send_group_message(sender_id, group_id, data["content"]):
            print("\033[96m" + "Message sending to group failed" + "\033[0m")
            return False

        # Send the message to all members of the group
        group_members = messages.get_group_members(group_id)
        if not group_members:
            print("\033[96m" + "No members found in the group" + "\033[0m")
            return False

        for member_id in group_members:
            member_sid = [sid for sid, user_id in users.items() if user_id == member_id]
            if not member_sid:
                print(
                    "\033[96m"
                    + f"Group member {member_id} is not connected"
                    + "\033[0m"
                )
                continue
            socketio.emit("message", data, room=member_sid[0])
