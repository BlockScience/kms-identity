OBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "rid": {"type": "string"},
        "transform": {
            "type": "object",
            "properties": {
                "reference": {"type": "string"},
                "from": {"type": "string"},
                "to": {"type": "string"}
            },
            "required": ["reference", "from", "to"]
        },
        "default_action": {"type": "string"}
    },
    "oneOf": [
        {
            "required": ["transform"],
            "not": {"required": ["rid"]}
        },
        {
            "required": ["rid"],
            "not": {"required": ["transform"]}
        }
    ]
}

UNDIRECTED_RELATION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "definition": {"type": "string"},
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
        "definition": {"type": "string"},
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
        "definition": {"type": "string"},
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
        "definition": {"type": "string"},
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
        "definition": {"type": "string"}
    }
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
                }
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
            }
        }
    }
}
