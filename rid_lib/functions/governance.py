from ..core import function
from ..functions.assertion import create_directed_assertion
from ..means import Object

@function(constructor=True, schema={
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "assertion": {"type": "string"},
        "agents": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["assertion", "agents"]
})
def create_governance(Means, context):
    rid = create_directed_assertion(Means, {
        "from": context.pop("agents"),
        "to": [context.pop("assertion")],
        **context
    })

    return rid

@function(schema={
    "type": "object",
    "properties": {
        "as": {"type": "string"},
        "action": {"type": "string"},
        "context": {"type": "object"}
    },
    "required": ["as", "action"]
})
def act(rid, context):
    agent_rid = context["as"]
    action_str = context["action"]
    action_context = context.get("context", None)

    gov_data = rid.read()

    assertion_rid = gov_data['to'][0]
    assertion = Object.from_string(rid=assertion_rid)

    agent_rids = gov_data['from']
    if agent_rid not in agent_rids:
        print(f"Agent {agent_rid} not authorized to act on assertion {assertion_rid}")
        return

    return getattr(assertion, action_str)(action_context)