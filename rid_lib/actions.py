from .means import *
from .functions import *

Object.set_actions({
    "from_string": from_string,
    "ingress": create_object,
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
    "update": update_assertion,
    "update_members": update_undirected_assertion_members,
    "delete": delete_assertion,
    "ingress": None,
    "refresh": None
})

DirectedAssertion.set_actions({
    "create": create_directed_assertion,
    "fork": fork_assertion,
    "read": read_directed_relation,
    "update": update_assertion,
    "update_members": update_directed_assertion_members,
    "delete": delete_assertion,
    "ingress": None,
    "refresh": None
})

URL.set_actions({
    "transform": transform_url,
    "dereference": dereference_url
})

HackMD.set_actions({
    "transform": transform_hackmd,
    "dereference": dereference_hackmd
})