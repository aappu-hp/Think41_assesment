from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), '../sql_app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Local imports
from app.models import User, Conversation, Message
from app.crud import (
    create_user, get_user,
    create_conversation, get_conversation,
    create_message, get_conversation_messages
)
from app.schemas import (
    UserSchema, ConversationSchema, MessageSchema
)

# Schema instances
user_schema         = UserSchema()
conversation_schema = ConversationSchema()
message_schema      = MessageSchema()
messages_schema     = MessageSchema(many=True)

# ------------------- ROUTES -------------------

@app.route('/users', methods=['POST'])
def post_user():
    data = request.get_json()
    if not data or not data.get('email'):
        abort(400, 'Email is required')
    try:
        user = create_user(db.session, data)
        return jsonify(user_schema.dump(user)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/conversations', methods=['POST'])
def post_conversation():
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id or not get_user(db.session, user_id):
        abort(404, 'Valid user_id required')
    conv = create_conversation(db.session, user_id)
    return jsonify(conversation_schema.dump(conv)), 201

@app.route('/conversations/<int:conv_id>/messages', methods=['GET'])
def get_messages(conv_id):
    if not get_conversation(db.session, conv_id):
        abort(404, 'Conversation not found')
    msgs = get_conversation_messages(db.session, conv_id)
    return jsonify(messages_schema.dump(msgs)), 200

@app.route('/conversations/<int:conv_id>/messages', methods=['POST'])
def post_message(conv_id):
    data = request.get_json()
    sender  = data.get('sender')
    content = data.get('content')
    if sender not in ('user', 'bot') or not content:
        abort(400, 'Invalid message data')
    if not get_conversation(db.session, conv_id):
        abort(404, 'Conversation not found')
    msg = create_message(db.session, conv_id, sender, content)
    return jsonify(message_schema.dump(msg)), 201

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')
    conv_id = data.get('conversation_id')

    if not user_id or not message:
        abort(400, 'user_id and message are required')

    user = get_user(db.session, user_id)
    if not user:
        abort(404, 'User not found')

    # Use existing conversation or create new one
    if conv_id:
        conv = get_conversation(db.session, conv_id)
        if not conv:
            abort(404, 'Conversation not found')
    else:
        conv = create_conversation(db.session, user_id)

    # Save user message
    user_msg = create_message(db.session, conv.id, 'user', message)

    # Generate AI response (placeholder)
    ai_response_text = f"Echo: {message}"  # Replace with real LLM call later
    ai_msg = create_message(db.session, conv.id, 'bot', ai_response_text)

    return jsonify({
        'conversation_id': conv.id,
        'messages': [
            message_schema.dump(user_msg),
            message_schema.dump(ai_msg)
        ]
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
