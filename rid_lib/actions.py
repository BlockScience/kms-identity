from .means import *
from .functions import *

RID.actions = {
    "from_string": from_string
}

UndirectedRelation.actions = {
    "create": create_undirected_relation,
    "read": read_relation,
    "delete": delete_relation
}

DirectedRelation.actions = {
    "create": create_directed_relation,
    "read": read_relation,
    "delete": delete_relation
}

UndirectedAssertion.actions = {
    "create": create_undirected_assertion,
    "fork": fork_assertion,
    "read": read_assertion,
    "update": update_assertion,
    "update_members": update_undirected_assertion_members,
    "delete": delete_assertion
}

DirectedAssertion.actions = {
    "create": create_directed_assertion,
    "fork": fork_assertion,
    "read": read_assertion,
    "update": update_assertion,
    "update_members": update_directed_assertion_members,
    "delete": delete_assertion
}

URL.actions = {
    "transform": transform_url,
    "dereference": dereference_hackmd
}

HackMD.actions = {
    "transform": transform_hackmd,
    "dereference": dereference_hackmd
}