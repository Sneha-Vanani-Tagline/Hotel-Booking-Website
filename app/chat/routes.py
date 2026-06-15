from . import chat
from app.auth.decorator import auth_required
from flask import redirect, url_for, render_template, flash, session, request
import app.services.hotel_service as hotel_S

@chat.route('/<int:id>', methods = ['GET', 'POST'])
@auth_required('user', 'host')
def messages(id):
    chats = hotel_S.getUser_Chat(id)
    conversations = hotel_S.getUser_Conversations(id)

    return render_template('messages.html', chats=chats, conversations = conversations)

