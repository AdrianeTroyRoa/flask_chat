from flask import request
from flask_socketio import emit, SocketIO
import random, time

from . import db
from .models import Message, LoggedIn

r = lambda: random.randint(0,255)
socketio = SocketIO()

users = {}
user_colors = {}

# In this case @param("connect") is an event
@socketio.on("connect")
def handle_connect():
    print("Client connected!")

def list_active():

    active_users = LoggedIn.query.filter(LoggedIn.date_out.is_(None)).order_by(LoggedIn.date_in.desc()).all()
    
    iter = 0;
    list_of_active = []
    while(iter<len(active_users)):
        list_of_active.append(active_users[iter].active_id)
        iter+=1

    emit("actives", list_of_active, broadcast=True)
    print("active user:", len(list_of_active))

@socketio.on("user_join")
def handle_user_join(username):
    isActive = LoggedIn.query.filter(LoggedIn.active_id==username).filter(LoggedIn.date_out.is_(None)).first()

    if not isActive:
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        new_session = LoggedIn(active_id=username, date_in=datetime)

        db.session.add(new_session)
        db.session.commit()
    
    list_active()

    messages = Message.query.order_by(Message.date).all()

    iter = 0;
    while(iter<len(messages)):
        message = messages[iter].content_text
        userid = messages[iter].sender_id
        emit("chat", {"message": message, "username": userid}, broadcast=False)
        iter+=1

    print(f"User {username} joined!")
    users[username] = request.sid
    print("we reached moon!")
    

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
