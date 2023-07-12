OBJECT_REFERENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "uri": {"type": "string"}
    },
    "required": ["uri"]
}

IDENTITY_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "type": {"type": "string"}
    },
    "required": ["name"]
}