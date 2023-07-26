OBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "rid": {"type": "string"},
        "default_action": {"type": "string"}
    },
    "required": ["rid"]
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
    "required": ["from", "to"],
    "additionalProperties": False
}

UNDIRECTED_ASSERTION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "members": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": [],
    "additionalProperties": False
}

DIRECTED_ASSERTION_SCHEMA = {
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
    "required": [],
    "additionalProperties": False
}