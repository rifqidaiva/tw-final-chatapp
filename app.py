from flask import Flask
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from datetime import timedelta
from users import users
from friendships import friendships
from messages import messages
from events import socketio

import sqlite3
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(friendships, url_prefix="/friendships")
app.register_blueprint(messages, url_prefix="/messages")

jwt = JWTManager(app)


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


if __name__ == "__main__":
    # Remove the database file if it exists
    if os.path.exists("chatapp.db"):
        os.remove("chatapp.db")

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    sqlStatement = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_by INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS group_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(group_id, user_id)
    );

    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER, -- NULL if message is sent to a group
        group_id INTEGER, -- NULL if message is sent to a user
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
        CHECK (
            (receiver_id IS NOT NULL AND group_id IS NULL) OR
            (receiver_id IS NULL AND group_id IS NOT NULL)
        )
    );

    CREATE TABLE IF NOT EXISTS friendships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user1_id INTEGER NOT NULL,
        user2_id INTEGER NOT NULL,
        status TEXT CHECK (status IN ('pending', 'accepted', 'blocked')) DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(user1_id, user2_id)
    );
    """

    cur.executescript(sqlStatement)
    conn.commit()
    conn.close()

    print("\033[96m" + "Database created successfully" + "\033[0m")

    socketio.init_app(app)
    socketio.run(app, debug=True)
