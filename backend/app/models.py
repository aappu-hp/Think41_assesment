# backend/app/models.py
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, DateTime, Text
)
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class DistributionCenter(Base):
    __tablename__ = 'distribution_centers'
    id        = Column(Integer, primary_key=True, index=True)
    name      = Column(String, nullable=False)
    latitude  = Column(Float)
    longitude = Column(Float)

class Product(Base):
    __tablename__ = 'products'
    id                     = Column(Integer, primary_key=True, index=True)
    cost                   = Column(Float)
    category               = Column(String)
    name                   = Column(String, nullable=False)
    brand                  = Column(String)
    retail_price           = Column(Float)
    department             = Column(String)
    sku                    = Column(String)
    distribution_center_id = Column(Integer, ForeignKey('distribution_centers.id'))
    distribution_center    = relationship('DistributionCenter', back_populates='products')

DistributionCenter.products = relationship('Product', back_populates='distribution_center')

class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id                             = Column(Integer, primary_key=True, index=True)
    product_id                     = Column(Integer, ForeignKey('products.id'))
    created_at                     = Column(DateTime)
    sold_at                        = Column(DateTime, nullable=True)
    cost                           = Column(Float)
    product_category               = Column(String)
    product_name                   = Column(String)
    product_brand                  = Column(String)
    product_retail_price           = Column(Float)
    product_department             = Column(String)
    product_sku                    = Column(String)
    product_distribution_center_id = Column(Integer)

    product = relationship('Product')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id                 = Column(Integer, primary_key=True, index=True)
    order_id           = Column(Integer, ForeignKey('orders.order_id'))
    user_id            = Column(Integer)
    product_id         = Column(Integer)
    inventory_item_id  = Column(Integer, ForeignKey('inventory_items.id'))
    status             = Column(String)
    created_at         = Column(DateTime)
    shipped_at         = Column(DateTime, nullable=True)
    delivered_at       = Column(DateTime, nullable=True)
    returned_at        = Column(DateTime, nullable=True)

    order          = relationship('Order', back_populates='items')
    inventory_item = relationship('InventoryItem')

class Order(Base):
    __tablename__ = 'orders'
    order_id    = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey('users.id'))
    status      = Column(String)
    gender      = Column(String)
    created_at  = Column(DateTime)
    returned_at = Column(DateTime, nullable=True)
    shipped_at  = Column(DateTime, nullable=True)
    delivered_at= Column(DateTime, nullable=True)
    num_of_item = Column(Integer)

    items = relationship('OrderItem', back_populates='order')

class User(Base):
    __tablename__ = 'users'
    id             = Column(Integer, primary_key=True, index=True)
    first_name     = Column(String)
    last_name      = Column(String)
    email          = Column(String, unique=True, index=True, nullable=False)
    age            = Column(Integer)
    gender         = Column(String)
    state          = Column(String)
    street_address = Column(String)
    postal_code    = Column(String)
    city           = Column(String)
    country        = Column(String)
    latitude       = Column(Float)
    longitude      = Column(Float)
    traffic_source = Column(String)
    created_at     = Column(DateTime)

    conversations = relationship('Conversation', back_populates='user')

class Conversation(Base):
    __tablename__ = 'conversations'
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey('users.id'))
    started_at = Column(DateTime, default=datetime.datetime.utcnow)

    user     = relationship('User', back_populates='conversations')
    messages = relationship('Message', back_populates='conversation')

class Message(Base):
    __tablename__ = 'messages'
    id              = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    sender          = Column(String, nullable=False)  # 'user' or 'bot'
    content         = Column(Text, nullable=False)
    timestamp       = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship('Conversation', back_populates='messages')
