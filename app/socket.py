from .extensions import socketio
from flask_socketio import send, emit, join_room, leave_room
from .booking import routes as booking_R
from .admin import routes as admin_R
from .host import routes as host_R
from flask import request, redirect, render_template,session
import app.services.hotel_service as hotel_S
import app.services.user_service as User_S

from datetime import datetime, timezone


@socketio.on('connect')
def connect():
    print('Socket connected.', datetime.now())

@socketio.on('disconnect')
def disconnect():
    User_S.makeUser_offline(session['user_id'])
    User_S.update_lastSeen(session['user_id'])

    print('Socket Disconnected')

@socketio.on('join_user')
def join_user(uid):
    
    join_room(f'user_{uid}')
    User_S.makeUser_online(uid)
    print(f'user_{uid} joined')

    has_unread_msg = hotel_S.checkUnreadMessages(uid, session['role'])
    print('in join_user event "FLask"', has_unread_msg)

    if has_unread_msg > 0:
        emit('display_msg_notification', has_unread_msg, to=f'user_{uid}')

@socketio.on('join_host')
def join_host(uid):
    
    join_room(f'host_{uid}')
    User_S.makeUser_online(uid)
    print(f'host_{uid} joined')
    has_unread_msg = hotel_S.checkUnreadMessages(uid, session['role'])
    print('in join_host event "FLask"', has_unread_msg)

    
    emit('display_msg_notification', has_unread_msg, to=f'host_{uid}')

@socketio.on('join_admin')
def join_admin():
   
    join_room(f'super_admin')
    
    emit('message', 'Super admin joined.')

@socketio.on('new_chat_message')
def save_message(data):
    
    msg_record = hotel_S.save_ChatMsg(cid = data['conversation_id'], sender = data['sender'], msg = data['msg'])
    
    conversation = hotel_S.getConversation_byId(data['conversation_id'])
    user = conversation.user
    host = User_S.getUserById(conversation.host_id)

    msgData = {
        'msg' : data['msg'],
        'sender': data['sender'],
        'created_at': msg_record.created_at.strftime('%I:%M %p'),
        'conversation_id': conversation.id
    }
    # print('message saved "FLASK"')

    emit('render_new_chat_message', msgData, to=f'user_{user.id}')

    emit('render_new_chat_message', msgData, to=f'host_{host.id}')

    # send notification 
    if data['sender'] == 'user':
        has_unread_msg = hotel_S.checkUnreadMessages(conversation.host_id, 'host')

        emit('display_msg_notification', has_unread_msg, to=f'host_{conversation.host_id}')
        # print(f'notification send to HOST "Flask"')

    elif data['sender'] == 'host':
        has_unread_msg = hotel_S.checkUnreadMessages(conversation.user_id, 'user')

        emit('display_msg_notification', has_unread_msg, to=f'user_{conversation.user_id}')
        # print(f'notification send to USER "Flask"')



@socketio.on('create_conversation')
def create_conversation(data):
    # print('new conversation in flask')
    result_id = hotel_S.create_Conversation(user_id = data['user_id'], host_id = data['host_id'], hotel_id = data['hotel_id'])

    socketio.emit('render_message_page', result_id, to=f'{session["role"]}_{session["user_id"]}')

@socketio.on('change_online_time')
def change_time(msg):
    session['last_online'] = datetime.now()

@socketio.on('makeAll_msg_asRead')
def readAll(cid, userRole):
    # print('makeAll_msg_asRead event occured in flask')
    if userRole == 'user':
        hotel_S.markAll_msg_Read(cid, 'host')
    else:
        hotel_S.markAll_msg_Read(cid, 'user')

    