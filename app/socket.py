from .extensions import socketio
from flask_socketio import send, emit, join_room, leave_room
from .booking import routes as booking_R
from .admin import routes as admin_R
from .host import routes as host_R
from flask import request, redirect, render_template,session


@socketio.on('connect')
def connect():
    print('Socket connected.')

@socketio.on('join_user')
def join_user(uid):
    
    join_room(f'user_{uid}')

    emit('message', f'User joined: {uid}')

@socketio.on('join_host')
def join_host(uid):
    
    join_room(f'host_{uid}')

    emit('message', f'Host joined: {uid}')

@socketio.on('join_admin')
def join_admin():
   
    join_room(f'super_admin')
    
    emit('message', 'Super admin joined.')

