from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from users import get_user_by_id

import sqlite3

friendships = Blueprint("friendships", __name__)


# MARK: Request
@friendships.route("/request", methods=["POST"])
@jwt_required()
def friend_request():
    data = request.get_json()
    user1_id = get_jwt_identity()
    user2_id = data.get("user2_id")

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    if user2_id is None:
        conn.close()
        return {"msg": "user2_id is required"}, 400

    if user1_id == user2_id:
        conn.close()
        return {"msg": "You cannot send a friend request to yourself"}, 400

    user2 = get_user_by_id(user2_id)
    if not user2:
        conn.close()
        return {"msg": "User does not exist"}, 404

    # Check if the friendship already exists
    cur.execute(
        "SELECT * FROM friendships WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)",
        (user1_id, user2_id, user2_id, user1_id),
    )
    existing_friendship = cur.fetchone()
    if existing_friendship:
        conn.close()
        return {"msg": "Friendship already exists"}, 409

    cur.execute(
        "INSERT INTO friendships (user1_id, user2_id) VALUES (?, ?);",
        (user1_id, user2_id),
    )
    conn.commit()
    conn.close()

    return {"msg": "Friendship requested successfully"}, 201


# MARK: Accept
@friendships.route("/accept", methods=["PUT"])
@jwt_required()
def accept():
    data = request.get_json()
    user1_id = get_jwt_identity()
    user2_id = data.get("user2_id")

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    if user2_id is None:
        conn.close()
        return {"msg": "user2_id is required"}, 400

    # Check if the friendship exists and is pending
    cur.execute(
        "SELECT status FROM friendships WHERE user1_id = ? AND user2_id = ?",
        (user2_id, user1_id),
    )
    existing_friendship = cur.fetchone()
    if not existing_friendship:
        conn.close()
        return {"msg": "Friendship does not exist"}, 404

    if existing_friendship[0] != "pending":
        conn.close()
        return {"msg": "Friendship is not in a pending state"}, 400

    cur.execute(
        "UPDATE friendships SET status = 'accepted' WHERE user1_id = ? AND user2_id = ?",
        (user2_id, user1_id),
    )
    conn.commit()
    conn.close()

    return {"msg": "Friendship accepted successfully"}, 200


# MARK: Remove
@friendships.route("/remove", methods=["DELETE"])
@jwt_required()
def remove():
    data = request.get_json()
    user1_id = get_jwt_identity()
    user2_id = data.get("user2_id")

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    if user2_id is None:
        conn.close()
        return {"msg": "user2_id is required"}, 400

    # Check if the friendship exists
    cur.execute(
        "SELECT * FROM friendships WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)",
        (user1_id, user2_id, user2_id, user1_id),
    )
    existing_friendship = cur.fetchone()
    if not existing_friendship:
        conn.close()
        return {"msg": "Friendship does not exist"}, 404

    cur.execute(
        "DELETE FROM friendships WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)",
        (user1_id, user2_id, user2_id, user1_id),
    )
    conn.commit()
    conn.close()

    return {"msg": "Friendship removed successfully"}, 200


# MARK: Friends list
@friendships.route("/list", methods=["GET"])
@jwt_required()
def list():
    user_id = get_jwt_identity()

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    cur.execute(
        """
        SELECT users.id, users.email, users.name, friendships.status
        FROM friendships
        JOIN users ON users.id = CASE 
            WHEN friendships.user1_id = ? THEN friendships.user2_id
            ELSE friendships.user1_id
        END
        WHERE (friendships.user1_id = ? OR friendships.user2_id = ?) 
        AND (friendships.status = 'accepted' OR (friendships.status = 'pending' AND friendships.user1_id = ?))
        """,
        (user_id, user_id, user_id, user_id),
    )
    friends = cur.fetchall()
    conn.close()

    friends_list = [
        {"id": friend[0], "email": friend[1], "name": friend[2], "status": friend[3]}
        for friend in friends
    ]

    return {
        "msg": "Friends and pending requests listed successfully",
        "friends": friends_list,
    }, 200


# MARK: Pending list
@friendships.route("/pending", methods=["GET"])
@jwt_required()
def pending():
    user_id = get_jwt_identity()

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    cur.execute(
        """
        SELECT users.id, users.email, users.name
        FROM friendships
        JOIN users ON users.id = friendships.user1_id
        WHERE friendships.user2_id = ? AND friendships.status = 'pending'
        """,
        (user_id,),
    )
    pending_requests = cur.fetchall()
    conn.close()

    pending_list = [
        {"id": request[0], "email": request[1], "name": request[2]}
        for request in pending_requests
    ]

    return {
        "msg": "Pending requests listed successfully",
        "pending_requests": pending_list,
    }, 200
