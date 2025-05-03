from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

import sqlite3

messages = Blueprint("messages", __name__)


# MARK: /get_messages
@messages.route("/get_messages", methods=["GET"])
@jwt_required()
def get_messages_route():
    data = request.get_json()
    user1_id = get_jwt_identity()
    user2_id = data.get("user2_id")

    if user2_id is None:
        return {"msg": "user2_id is required"}, 400

    raw_messages = get_messages(user1_id, user2_id)
    messages = [
        {
            "sender_id": msg[0],
            "receiver_id": msg[1],
            "content": msg[2],
            "timestamp": msg[3],
            "is_sender": msg[0] == user1_id,
        }
        for msg in raw_messages
    ]
    return {"messages": messages, "msg": "Messages retrieved successfully"}, 200


# MARK: /get_group_messages
@messages.route("/get_group_messages", methods=["GET"])
@jwt_required()
def get_group_messages_route():
    data = request.get_json()
    group_id = data.get("group_id")
    user_id = get_jwt_identity()

    if group_id is None:
        return {"msg": "group_id is required"}, 400

    # Check if the user is a member of the group
    group_members = get_group_members(group_id)
    if not any(member[0] == user_id for member in group_members):
        return {"msg": "You are not a member of this group"}, 403

    raw_messages = get_group_messages(group_id)
    messages = [
        {
            "sender_id": msg[0],
            "group_id": msg[1],
            "content": msg[2],
            "timestamp": msg[3],
            "is_sender": msg[0] == user_id,
        }
        for msg in raw_messages
    ]
    return {"messages": messages, "msg": "Messages retrieved successfully"}, 200


def send_message(sender_id: int, receiver_id: int, content: str) -> bool:
    """
    Send a message from the sender to the receiver.
    """
    if sender_id == receiver_id:
        return False

    if not content.strip():
        return False

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    # Check if the receiver exists
    cur.execute("SELECT id FROM users WHERE id = ?", (receiver_id,))
    if cur.fetchone() is None:
        return False

    cur.execute(
        "INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
        (sender_id, receiver_id, content),
    )
    conn.commit()
    conn.close()

    return True


def send_group_message(sender_id: int, group_id: int, content: str) -> bool:
    """
    Send a message from the sender to the group.
    """
    if not content.strip():
        return False

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    # Check if the group exists
    cur.execute("SELECT id FROM groups WHERE id = ?", (group_id,))
    if cur.fetchone() is None:
        conn.close()
        return False

    cur.execute(
        "INSERT INTO messages (sender_id, group_id, content) VALUES (?, ?, ?)",
        (sender_id, group_id, content),
    )
    conn.commit()
    conn.close()

    return True


def get_messages(user_id: int, other_id: int) -> list:
    """
    Get messages between two users.

    Return example:

    [
        (sender_id, receiver_id, content, timestamp),
        (sender_id, receiver_id, content, timestamp),
        ...
    ]
    """
    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    cur.execute(
        """
        SELECT sender_id, receiver_id, content, timestamp
        FROM messages
        WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
        ORDER BY timestamp
        """,
        (user_id, other_id, other_id, user_id),
    )
    messages = cur.fetchall()

    conn.close()

    return messages


def get_group_messages(group_id: int) -> list:
    """
    Get messages in a group.

    Return example:

    [
        (sender_id, group_id, content, timestamp),
        (sender_id, group_id, content, timestamp),
        ...
    ]
    """
    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    cur.execute(
        """
        SELECT sender_id, group_id, content, timestamp
        FROM messages
        WHERE group_id = ?
        ORDER BY timestamp
        """,
        (group_id,),
    )
    messages = cur.fetchall()

    conn.close()

    return messages


def get_group_members(group_id: int) -> list:
    """
    Get members of a group.

    Return example:

    [
        (user_id, name),
        (user_id, name),
        ...
    ]
    """
    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    cur.execute(
        """
        SELECT users.id, users.name
        FROM users
        JOIN group_members ON users.id = group_members.user_id
        WHERE group_members.group_id = ?
        """,
        (group_id,),
    )
    members = cur.fetchall()

    conn.close()

    return members
