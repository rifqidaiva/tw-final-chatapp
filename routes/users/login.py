import flask
import flask_jwt_extended
import bcrypt
import sqlite3

from .utils import is_valid_password, is_valid_email
import utils


def login():
    data = flask.request.get_json()
    input_email = data.get("email")
    input_password = data.get("password")

    if input_email is None or input_password is None:
        return utils.Response(
            status_code=400,
            msg="Email and password are required",
        ).send()

    # Validate email
    if not is_valid_email(input_email):
        return utils.Response(
            status_code=400,
            msg="Invalid email format according to RFC 5322",
        ).send()

    # Validate password
    if not is_valid_password(input_password):
        return utils.Response(
            status_code=400,
            msg="Password must be at least 8 characters long, contain at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character (can be any non-alphanumeric character). No spaces are allowed",
        ).send()

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (input_email,))
    row = cur.fetchone()
    conn.close()

    # Check if the user exists
    user = utils.User.from_row(row) if row else None

    if user is None:
        conn.close()
        return utils.Response(
            status_code=401,
            msg="Invalid email or password",
        ).send()

    # Check if the password is correct
    if not user.password or not bcrypt.checkpw(
        input_password.encode(), user.password.encode()
    ):
        conn.close()
        return utils.Response(
            status_code=401,
            msg="Invalid email or password",
        ).send()

    # Generate JWT token
    access_token = flask_jwt_extended.create_access_token(identity=str(user.id))
    refresh_token = flask_jwt_extended.create_refresh_token(identity=str(user.id))

    return utils.Response(
        status_code=200,
        msg="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "profile_picture": user.profile_picture,
                "created_at": user.created_at,
            },
        },
    ).send()
