from .means import *
from .functions import *

RID.set_actions({
    "from_string": from_string,
    "ingress": create_object
})

UndirectedRelation.set_actions({
    "create": create_undirected_relation,
    "read": read_relation,
    "delete": delete_relation
})

DirectedRelation.set_actions({
    "create": create_directed_relation,
    "read": read_relation,
    "delete": delete_relation
})

UndirectedAssertion.set_actions({
    "create": create_undirected_assertion,
    "fork": fork_assertion,
    "read": read_assertion,
    "update": update_assertion,
    "update_members": update_undirected_assertion_members,
    "delete": delete_assertion
})

DirectedAssertion.set_actions({
    "create": create_directed_assertion,
    "fork": fork_assertion,
    "read": read_assertion,
    "update": update_assertion,
    "update_members": update_directed_assertion_members,
    "delete": delete_assertion
})

URL.set_actions({
    "transform": transform_url,
    "dereference": dereference_hackmd
})

HackMD.set_actions({
    "transform": transform_hackmd,
    "dereference": dereference_hackmd
})