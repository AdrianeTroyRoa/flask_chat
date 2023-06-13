from flask import request
from flask_socketio import emit
from flask_socketio import SocketIO
import random

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

    check_color(user_colors, username)
    emit("chat", {"message": message, "username": username, "color": user_colors[username]}, broadcast=True)
    
