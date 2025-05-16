import flask
import bcrypt
import sqlite3

from .utils import is_valid_password, is_valid_email, is_valid_name
import utils


def register():
    data = flask.request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if email is None or password is None or name is None:
        return utils.Response(
            status_code=400,
            msg="Email, password, and name are required",
        ).send()

    # Validate email
    if not is_valid_email(email):
        return utils.Response(
            status_code=400,
            msg="Invalid email format according to RFC 5322",
        ).send()

    # Validate password
    if not is_valid_password(password):
        return utils.Response(
            status_code=400,
            msg="Password must be at least 8 characters long, contain at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character (can be any non-alphanumeric character). No spaces are allowed",
        ).send()

    # Check if the name is valid
    if not is_valid_name(name):
        return utils.Response(
            status_code=400,
            msg="Name must be 3-20 characters long, can contain letters, numbers, underscores, and hyphens. It cannot start or end with an underscore or hyphen",
        ).send()

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    # Check if the email is already registered
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        conn.close()
        return utils.Response(
            status_code=409,
            msg="Email is already registered",
        ).send()

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))

    sqlStatement = """
    INSERT INTO users (email, password, name) VALUES (?, ?, ?);
    """

    cur.execute(sqlStatement, (email, hashed_password.decode(), name))
    conn.commit()
    conn.close()

    return utils.Response(
        status_code=201,
        msg="User registered successfully",
    ).send()
