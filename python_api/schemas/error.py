"""JSON-схемы для ответов с ошибками."""


# Fastify-ошибки (например, 400 на невалидный UUID)
FASTIFY_ERROR_SCHEMA = {
    "type": "object",
    "required": ["statusCode", "code", "error", "message"],
    "properties": {
        "statusCode": {"type": "integer"},
        "code":       {"type": "string"},
        "error":      {"type": "string"},
        "message":    {"type": "string"},
    },
}


# Универсальная ошибка (например, 404 Not Found)
GENERIC_ERROR_SCHEMA = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string"},
    },
}