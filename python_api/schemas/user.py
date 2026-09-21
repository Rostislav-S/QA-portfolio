"""JSON-схемы для ресурса users."""

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "role", "created_at"],
    "properties": {
        "id":         {"type": "string"},
        "name":       {"type": "string"},
        "email":      {"type": "string"},
        "role":       {"type": "string"},
        "created_at": {"type": "string"},
    },
}


USERS_LIST_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["success", "data", "pagination"],
    "properties": {
        "success": {"type": "boolean"},
        "data": {
            "type": "array",
            "items": USER_SCHEMA,
        },
        "pagination": {"type": "object"},
    },
}


SINGLE_USER_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["success", "data"],
    "properties": {
        "success": {"type": "boolean"},
        "data":    USER_SCHEMA,
    },
}