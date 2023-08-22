DEFAULT_RID_STR_SCHEMA = {
    "type": "object",
    "properties": {
        "rid": {"type": "string"}
    },
    "required": ["rid"]
}

TRANSFORMER_CONTEXT_SCHEMA = {
    "type": "object",
    "properties": {
        "means": {"type": "string"}
    },
    "required": ["means"]
}