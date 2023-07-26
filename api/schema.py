OBJECT_REFERENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "reference": {"type": "string"},
        "dereferencer": {"type": "string"}
    },
    "required": ["reference"]
}

OBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "rid": {"type": "string"},
        "default_action": {"type": "string"}
    },
    "required": ["rid"]
}

DIRECTED_RELATION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "from": {
            "type": "array",
            "items": {"type": "string"}
        },
        "to": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["from", "to"]
}

UNDIRECTED_RELATION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "members": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["members"],
    "additionalProperties": False
}

ASSERTION_SCHEMA = {
    "type": "object",
    "properties": {
        "rid": {"type": "string"},
        "type": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"}
    },
    "required": ["type"]
}

IDENTITY_SCHEMA = {
    "type": "object",
    "properties": {
        "rid": {"type": "string"},
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
