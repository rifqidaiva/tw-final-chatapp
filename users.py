from flask import Blueprint
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

import sqlite3
import bcrypt
import re

users = Blueprint("users", __name__)


# MARK: Register
@users.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if email is None or password is None or name is None:
        return {"msg": "Email, password, and name are required."}, 400

    # Validate email
    if not is_valid_email(email):
        return {"msg": "Invalid email format according to RFC 5322."}, 400

    # Validate password
    if not is_valid_password(password):
        return (
            {
                "msg": "Password must be at least 8 characters long, contain at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character (can be any non-alphanumeric character). No spaces are allowed."
            },
            400,
        )

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    # Check if the email is already registered
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        conn.close()
        return {"msg": "Email is already registered."}, 409

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))

    sqlStatement = """
    INSERT INTO users (email, password, name) VALUES (?, ?, ?);
    """

    cur.execute(sqlStatement, (email, hashed_password.decode(), name))
    conn.commit()
    conn.close()

    return {"msg": "User registered successfully."}, 201


# MARK: Login
@users.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email is None or password is None:
        return {"msg": "Email and password are required."}, 400

    # Validate email
    if not is_valid_email(email):
        return {"msg": "Invalid email format according to RFC 5322."}, 400

    # Validate password
    if not is_valid_password(password):
        return (
            {
                "msg": "Password must be at least 8 characters long, contain at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character (can be any non-alphanumeric character). No spaces are allowed."
            },
            400,
        )

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()

    if user is None or not bcrypt.checkpw(password.encode(), user[2].encode()):
        return {"msg": "Invalid email or password."}, 401

    # Use the user's ID as the identity in the JWT
    access_token = create_access_token(identity=str(user[0]))

    return {
        "msg": "Login successful.",
        "access_token": access_token,
    }, 200


# MARK: Data
@users.route("/data", methods=["GET"])
@jwt_required()
def data():
    """Get user information from the token."""
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)

    if user is None:
        return {"msg": "User not found."}, 404

    print(user)

    return {
        "msg": "User data retrieved successfully.",
        "id": user[0],
        "email": user[1],
        "name": user[3],
    }, 200


@users.route("/logout")
def logout():
    return "Logout"


@users.route("/profile")
def profile():
    return "Profile"


def is_valid_email(email: str) -> bool:
    """
    Validate email format according to RFC 5322.
    """
    pattern = (
        r"^(?!.*\.\.)([a-zA-Z0-9][a-zA-Z0-9._%+-]{0,63})@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    return re.fullmatch(pattern, email) is not None


def is_valid_password(password: str) -> bool:
    """Password must be at least 8 characters long,
    contain at least 1 uppercase letter, 1 lowercase letter, 1 number,
    and 1 special character (can be any non-alphanumeric character).
    No spaces are allowed.
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])\S{8,}$"
    return re.fullmatch(pattern, password) is not None


def get_user_by_id(user_id: int):
    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()

    return user
