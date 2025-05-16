from flask_socketio import SocketIO

socketio = SocketIO(async_mode="eventlet")
users = {}


@socketio.on("connect")
def connect():
    print("Client connected")
