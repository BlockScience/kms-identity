OBJECT_JSON_ENDPOINT_SCHEMA = {
    "type": "object",
    "properties": {
        "rid": {"type": "string"},
        "action": {"type": "string"},
        "context": {"type": "object"}
    },
    "required": ["rid", "action"]
}

OBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "rid": {
            "oneOf": [
                {"type": "string"},
                {
                    "type": "array",
                    "items": {"type": "string"}
                },
                {
                    "type": "object",
                    "properties": {
                        "means": {"type": "string"},
                        "reference": {"type": "string"}
                    },
                    "required": ["means", "reference"]
                }
            ]
        },
        "transform": {"type": "string"}
    },
    "required": ["rid"]
}

UNDIRECTED_RELATION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "definition": {"type": ["string", "null"]},
        "members": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

DIRECTED_RELATION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "definition": {"type": ["string", "null"]},
        "from": {
            "type": "array",
            "items": {"type": "string"}
        },
        "to": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

UNDIRECTED_ASSERTION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "definition": {"type": ["string", "null"]},
        "members": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

DIRECTED_ASSERTION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "definition": {"type": ["string", "null"]},
        "from": {
            "type": "array",
            "items": {"type": "string"}
        },
        "to": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

UPDATE_ASSERTION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"}
    },
    "additionalProperties": True,
    "not": {
        "properties": {
            "rid": {},
            "members": {},
            "from": {},
            "to": {}
        },
        "additionalProperties": False
    }
}

UPDATE_ASSERTION_DEFINITION_SCHEMA = {
    "type": "object",
    "properties": {
        "definition": {"type": ["string", "null"]}
    },
    "required": ["definition"]
}

UPDATE_UNDIRECTED_ASSERTION_MEMBERS_SCHEMA = {
    "type": "object",
    "properties": {
        "add": {
            "type": "array",
            "items": {"type": "string"}
        },
        "remove": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

UPDATE_DIRECTED_ASSERTION_MEMBERS_SCHEMA = {
    "type": "object",
    "properties": {
        "add": {
            "type": "object",
            "properties": {
                "from": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "to": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "additionalProperties": False
            }
        },
        "remove": {
            "type": "object",
            "properties": {
                "from": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "to": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "additionalProperties": False
        },
        "additionalProperties": False
    }
}
