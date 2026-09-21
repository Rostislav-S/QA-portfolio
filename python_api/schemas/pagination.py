"""JSON-схема для блока pagination."""

PAGINATION_SCHEMA = {
    "type": "object",
    "required": ["total", "page", "limit", "pages", "hasNext", "hasPrev"],
    "properties": {
        "total":   {"type": "integer"},
        "page":    {"type": "integer"},
        "limit":   {"type": "integer"},
        "pages":   {"type": "integer"},
        "hasNext": {"type": "boolean"},
        "hasPrev": {"type": "boolean"},
    },
}