# app/schemas.py
from marshmallow import Schema, fields

# Marshmallow schema for serialization/deserialization
class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    completed = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)


# Swagger/OpenAPI definition for Flasgger
swagger_definitions = {
    'Task': {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "completed": {"type": "boolean"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"},
            "user_id": {"type": "integer"}
        }
    }
}
