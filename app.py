import flask
import flask_jwt_extended
import datetime
import sqlite3
import os

import events
import utils
import routes.users
import routes.friendships
import routes.messages

app = flask.Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "pdf", "docx", "txt"}
app.register_blueprint(routes.users.users, url_prefix="/users")
app.register_blueprint(routes.friendships.friendships, url_prefix="/friendships")
app.register_blueprint(routes.messages.messages, url_prefix="/messages")

jwt = flask_jwt_extended.JWTManager(app)


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


if __name__ == "__main__":
    # Remove the database file if it exists
    if os.path.exists("chatapp.db"):
        os.remove("chatapp.db")

    # Remove the uploads directory if it exists
    if os.path.exists("uploads"):
        for root, dirs, files in os.walk("uploads", topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    sqlStatement = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        profile_picture TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        content TEXT,
        file_path TEXT,
        file_name TEXT,
        file_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
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

    utils.log(message="Database created successfully")

    events.socketio.init_app(app)
    events.socketio.run(app, debug=True)
