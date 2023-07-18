OBJECT_REFERENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "reference": {"type": "string"},
        "dereferencer": {"type": "string"}
    },
    "required": ["reference"]
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

UPDATE_IDENTITY_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "type": {"type": "string"}
    }
}
