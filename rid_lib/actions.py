from .means import *
from .functions import *

Object.set_actions({
    "from_string": from_string,
    "ingress": create_object,
    "exists": object_exists,
    "read": read_object,
    "refresh": refresh_object
})

UndirectedRelation.set_actions({
    "create": create_undirected_relation,
    "read": read_undirected_relation,
    "delete": delete_relation,
    "ingress": None,
    "refresh": None
})

DirectedRelation.set_actions({
    "create": create_directed_relation,
    "read": read_directed_relation,
    "delete": delete_relation,
    "ingress": None,
    "refresh": None
})

UndirectedAssertion.set_actions({
    "create": create_undirected_assertion,
    "fork": fork_assertion,
    "read": read_undirected_relation,
    "read_transactions": read_transactions,
    "update": update_assertion,
    "update_definition": update_assertion_definition,
    "update_members": update_undirected_assertion_members,
    "delete": delete_assertion,
    "ingress": None,
    "refresh": None
})

DirectedAssertion.set_actions({
    "create": create_directed_assertion,
    "fork": fork_assertion,
    "read": read_directed_relation,
    "read_transactions": read_transactions,
    "update": update_assertion,
    "update_definition": update_assertion_definition,
    "update_members": update_directed_assertion_members,
    "delete": delete_assertion,
    "ingress": None,
    "refresh": None
})

Agent.set_actions({
    "create": create_agent
})

Governance.set_actions({
    "create": create_governance,
    "act": act
})

Belief.set_actions({
    "set": set_belief
})

URL.set_actions({
    "transform": transform_url,
    "dereference": dereference_url
})

HackMD.set_actions({
    "transform": transform_hackmd,
    "dereference": dereference_hackmd
})