from marshmallow import Schema, fields, post_dump

class UserSchema(Schema):
    id         = fields.Int(dump_only=True)
    email      = fields.Email(required=True)
    first_name = fields.Str()
    last_name  = fields.Str()

class MessageSchema(Schema):
    id              = fields.Int(dump_only=True)
    conversation_id = fields.Int(required=True)
    sender          = fields.Str(required=True)
    content         = fields.Str(required=True)
    timestamp       = fields.DateTime()

class ConversationSchema(Schema):
    id         = fields.Int(dump_only=True)
    user_id    = fields.Int(required=True)
    started_at = fields.DateTime()
    messages   = fields.List(fields.Nested(MessageSchema))

    @post_dump
    def sort_messages(self, data, **kwargs):
        # ensure chronological order
        data['messages'].sort(key=lambda m: m['timestamp'])
        return data
