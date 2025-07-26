from datetime import datetime
from app.models import User, Conversation, Message

def create_user(db, data):
    # Avoid duplicate users based on unique email
    existing = db.query(User).filter_by(email=data['email']).first()
    if existing:
        return existing  # Return existing user if email already exists

    user = User(
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        age=data.get('age'),
        gender=data.get('gender'),
        state=data.get('state'),
        street_address=data.get('street_address'),
        postal_code=data.get('postal_code'),
        city=data.get('city'),
        country=data.get('country'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        traffic_source=data.get('traffic_source'),
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()

def create_conversation(db, user_id):
    conv = Conversation(user_id=user_id, started_at=datetime.utcnow())
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_conversation(db, conv_id):
    return db.query(Conversation).filter(Conversation.id == conv_id).first()

def create_message(db, conv_id, sender, content):
    msg = Message(
        conversation_id=conv_id,
        sender=sender,
        content=content,
        timestamp=datetime.utcnow()
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_conversation_messages(db, conv_id):
    return (
        db.query(Message)
        .filter(Message.conversation_id == conv_id)
        .order_by(Message.timestamp)
        .all()
    )
