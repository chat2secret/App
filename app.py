from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_ALLOWED_ORIGINS'] = '*'
socketio = SocketIO(app, cors_allowed_origins="*")

# Simple in-memory storage for messages
messages = {
    "user1": [],
    "user2": []
}

# Store online users
online_users = {
    "user1": False,
    "user2": False
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/messages/<user>', methods=['GET'])
def get_messages(user):
    if user in ['user1', 'user2']:
        return jsonify(messages[user])
    return jsonify({"error": "Invalid user"}), 400

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('set_user')
def handle_set_user(data):
    user = data.get('user')
    if user in ['user1', 'user2']:
        online_users[user] = True
        emit('user_status', {'user': user, 'status': 'online'}, broadcast=True)
        print(f'{user} is now online')

@socketio.on('user_offline')
def handle_user_offline(data):
    user = data.get('user')
    if user in ['user1', 'user2']:
        online_users[user] = False
        emit('user_status', {'user': user, 'status': 'offline'}, broadcast=True)
        print(f'{user} is now offline')

@socketio.on('send_message')
def handle_send_message(data):
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')
    
    if sender not in ['user1', 'user2'] or receiver not in ['user1', 'user2']:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_data = {
        'sender': sender,
        'receiver': receiver,
        'message': message,
        'timestamp': timestamp
    }
    
    # Store message for both users
    messages[sender].append(message_data)
    messages[receiver].append(message_data)
    
    # Emit to both users
    emit('receive_message', message_data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
