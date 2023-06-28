from flask import request
from flask_socketio import emit
from flask_socketio import SocketIO
import random

from . import db
from .models import Message

import time 

r = lambda: random.randint(0,255)
socketio = SocketIO()

users = {}
user_colors = {}

# In this case @param("connect") is an event
@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    messages = Message.query.order_by(Message.date).all()

    iter = 0;
    while(iter<len(messages)):
        message = messages[iter].content_text
        userid = messages[iter].sender_id
        emit("chat", {"message": message, "username": userid}, broadcast=False)
        iter+=1

    print(f"User {username} joined!")
    users[username] = request.sid
    

def check_color(dictionary, username):
    for keys in dictionary.keys():
        if (keys == username):
            return;
    color = '#%02X%02X%02X' % (r(),r(),r())
    user_colors[username] = color

@socketio.on("new_message")
def handle_new_message(message):
    if(message == ""):
        return 

    message_len = len(message)
    iteration = 1
    for char in message:
        if(char != " "):
            break
        elif(message_len == iteration):
            return
        else:
            iteration+=1

    print(f"New message: {message}")
    username = None
    for user in users:
        if users[user] == request.sid:
            username = user

    emit("chat", {"message": message, "username": username}, broadcast=True)
    datetime = time.strftime('%Y-%m-%d %H:%M:%S')
    new_message = Message(sender_id=username, date=datetime, content_text=message)

    db.session.add(new_message)
    db.session.commit()
   
