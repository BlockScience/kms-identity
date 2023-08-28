from ..core import function
from ..functions.assertion import create_directed_assertion

@function(
    constructor=True,
    schema={
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "object": {"type": "string"},
            "value": {"type": "number"}
        },
        "required": ["agent", "object", "value"]
    }
)
def set_belief(Means, context):
    agent = context.pop("agent")
    obj = context.pop("object")
    value = context.pop("value")
    reference = f"[{agent}]->[{obj}]"

    rid = Means(reference)

    if rid.exists():
        rid.update(value=value)

    else:
        rid = create_directed_assertion(Means, {
            "reference": reference,
            "value": value,
            "from": [agent],
            "to": [obj],
            **context
        })

    return rid