from flask import Flask, redirect, render_template, url_for, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret'

socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username
    join_room(username)
    emit('message', f'{username} joined the chat', room = username)

@socketio.on('message')
def handle_message(data):
    username = users.get(request.sid, 'Anonymous')
    emit('message', f'{username} : {data}', broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = users.get(request.sid, 'Anonymous')
    emit('message', f'{username} left the chat.', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)