# backend/app/app.py

import os
import json
from venv import logger
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from .database import SessionLocal, Base, engine
from .models import (
    DistributionCenter, Product, InventoryItem,
    Order, OrderItem, User, Conversation, Message
)
from .schemas import (
    DistributionCenterSchema, ProductSchema,
    InventoryItemSchema, OrderSchema, OrderItemSchema,
    UserSchema, ConversationSchema, MessageSchema
)
from .crud import get_all, get_by_id, create
from app.llm_chain import run_query  # Updated import

app = Flask(__name__)
CORS(app)

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# — Milestones 1–2: Data Endpoints —

@app.route('/api/distribution_centers', methods=['GET'])
def list_distribution_centers():
    sess = SessionLocal()
    items = get_all(sess, DistributionCenter)
    data = DistributionCenterSchema(many=True).dump(items)
    sess.close()
    return jsonify(data), 200

@app.route('/api/products', methods=['GET'])
def list_products():
    sess = SessionLocal()
    items = get_all(sess, Product)
    data = ProductSchema(many=True).dump(items)
    sess.close()
    return jsonify(data), 200

@app.route('/api/inventory_items', methods=['GET'])
def list_inventory_items():
    sess = SessionLocal()
    items = get_all(sess, InventoryItem)
    data = InventoryItemSchema(many=True).dump(items)
    sess.close()
    return jsonify(data), 200

@app.route('/api/orders', methods=['GET'])
def list_orders():
    sess = SessionLocal()
    items = get_all(sess, Order)
    data = OrderSchema(many=True).dump(items)
    sess.close()
    return jsonify(data), 200

@app.route('/api/order_items', methods=['GET'])
def list_order_items():
    sess = SessionLocal()
    items = get_all(sess, OrderItem)
    data = OrderItemSchema(many=True).dump(items)
    sess.close()
    return jsonify(data), 200

# — Milestone 3: Conversations & Messages —

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'email' not in data:
        abort(400, description="email is required")
    sess = SessionLocal()
    user = create(sess, User(**data))
    sess.close()
    return jsonify(UserSchema().dump(user)), 201

@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    data = request.get_json()
    uid = data.get("user_id")
    if not uid:
        abort(400, description="user_id is required")
    sess = SessionLocal()
    if not get_by_id(sess, User, uid):
        sess.close()
        abort(404, description="User not found")
    conv = create(sess, Conversation(user_id=uid))
    sess.close()
    return jsonify(ConversationSchema().dump(conv)), 201

@app.route('/api/conversations/<int:cid>/messages', methods=['GET'])
def get_conversation_messages(cid):
    sess = SessionLocal()
    conv = get_by_id(sess, Conversation, cid)
    if not conv:
        sess.close()
        abort(404, description="Conversation not found")
    msgs = conv.messages
    data = MessageSchema(many=True).dump(msgs)
    sess.close()
    return jsonify(data), 200

@app.route('/api/conversations/<int:cid>/messages', methods=['POST'])
def post_message(cid):
    data = request.get_json()
    sess = SessionLocal()
    conv = get_by_id(sess, Conversation, cid)
    if not conv:
        sess.close()
        abort(404, description="Conversation not found")
    msg = create(sess, Message(
        conversation_id=cid,
        sender=data.get("sender"),
        content=data.get("content")
    ))
    sess.close()
    return jsonify(MessageSchema().dump(msg)), 201

# — Milestone 4 & 5: Core Chatbot Endpoint —

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    
    # === Log the raw request for debugging ===
    logger.info(f"Incoming /api/chat request JSON: {data!r}")
    
    user_id = data.get('user_id')
    message = data.get('message')
    conv_id = data.get('conversation_id')

    if not user_id or not message:
        abort(400, "user_id and message are required")

    sess = SessionLocal()
    try:
        # Validate user
        user = get_by_id(sess, User, user_id)
        if not user:
            abort(404, "User not found")

        # Reuse or create conversation
        if conv_id:
            conversation = get_by_id(sess, Conversation, conv_id)
            if not conversation:
                abort(404, "Conversation not found")
        else:
            conversation = create(sess, Conversation(user_id=user_id))

        conversation_id = conversation.id
        
        # Save the user's message
        user_msg = create(sess, Message(
            conversation_id=conversation_id,
            sender="user",
            content=message
        ))

        # Build conversation history for context
        history_messages = (
            sess.query(Message)
                .filter(Message.conversation_id == conversation_id)
                .order_by(Message.timestamp.asc())
                .all()
        )
        history_str = "\n".join(
            f"{m.sender}: {m.content}" for m in history_messages
        )

        # Log the history and current message
        logger.info(f"Conversation #{conversation_id} history:\n{history_str}")
        logger.info(f"Generating AI reply for message: {message!r}")

        # Generate AI response
        ai_reply = run_query(
            f"Conversation history:\n{history_str}\n\nCurrent message: {message}"
        )
        logger.info(f"AI replied: {ai_reply!r}")

        # Save the bot's reply
        bot_msg = create(sess, Message(
            conversation_id=conversation_id,
            sender="bot",
            content=ai_reply
        ))

        sess.commit()

        return jsonify({
            "conversation_id": conversation_id,
            "user_message": message,
            "ai_response": ai_reply
        }), 200

    except Exception as e:
        sess.rollback()
        logger.exception("Error in /api/chat")
        return jsonify({"error": str(e)}), 500

    finally:
        sess.close()
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)