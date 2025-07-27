# backend/app/schemas.py
from marshmallow import Schema, fields

class DistributionCenterSchema(Schema):
    id        = fields.Int()
    name      = fields.Str()
    latitude  = fields.Float()
    longitude = fields.Float()

class ProductSchema(Schema):
    id                     = fields.Int()
    cost                   = fields.Float()
    category               = fields.Str()
    name                   = fields.Str()
    brand                  = fields.Str()
    retail_price           = fields.Float()
    department             = fields.Str()
    sku                    = fields.Str()
    distribution_center_id = fields.Int()

class InventoryItemSchema(Schema):
    id                            = fields.Int()
    product_id                    = fields.Int()
    created_at                    = fields.DateTime()
    sold_at                       = fields.DateTime(allow_none=True)
    cost                          = fields.Float()
    product_category              = fields.Str()
    product_name                  = fields.Str()
    product_brand                 = fields.Str()
    product_retail_price          = fields.Float()
    product_department            = fields.Str()
    product_sku                   = fields.Str()
    product_distribution_center_id= fields.Int()

class OrderSchema(Schema):
    order_id    = fields.Int()
    user_id     = fields.Int()
    status      = fields.Str()
    gender      = fields.Str()
    created_at  = fields.DateTime()
    returned_at = fields.DateTime(allow_none=True)
    shipped_at  = fields.DateTime(allow_none=True)
    delivered_at= fields.DateTime(allow_none=True)
    num_of_item = fields.Int()

class OrderItemSchema(Schema):
    id                = fields.Int()
    order_id          = fields.Int()
    user_id           = fields.Int()
    product_id        = fields.Int()
    inventory_item_id = fields.Int()
    status            = fields.Str()
    created_at        = fields.DateTime()
    shipped_at        = fields.DateTime(allow_none=True)
    delivered_at      = fields.DateTime(allow_none=True)
    returned_at       = fields.DateTime(allow_none=True)

class UserSchema(Schema):
    id             = fields.Int()
    first_name     = fields.Str()
    last_name      = fields.Str()
    email          = fields.Email()
    age            = fields.Int()
    gender         = fields.Str()
    state          = fields.Str()
    street_address = fields.Str()
    postal_code    = fields.Str()
    city           = fields.Str()
    country        = fields.Str()
    latitude       = fields.Float()
    longitude      = fields.Float()
    traffic_source = fields.Str()
    created_at     = fields.DateTime()

class MessageSchema(Schema):
    id              = fields.Int()
    conversation_id = fields.Int()
    sender          = fields.Str()
    content         = fields.Str()
    timestamp       = fields.DateTime()

class ConversationSchema(Schema):
    id         = fields.Int()
    user_id    = fields.Int()
    started_at = fields.DateTime()
    messages   = fields.List(fields.Nested(MessageSchema))
