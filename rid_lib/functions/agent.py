from ..core import *
from api import database

@function(
    constructor=True,
    schema={
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
)
def create_agent(Means, context):
    name = context.get("name")
    rid = Means(name)
    database.assertions.create_undirected(rid, context)
    return rid