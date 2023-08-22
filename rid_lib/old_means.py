from rid_lib.rids import *
from rid_lib.functions import *

UndirectedRelation.actions = {
    "create": CreateUndirectedRelation,
    "read": ReadRelation,
    "delete": DeleteRelation
}

class DirectedRelation(Means):
    symbol = DIRECTED_RELATION
    actions = {
        "create": CreateDirectedRelation,
        "read": ReadRelation,
        "delete": DeleteRelation
    }

class UndirectedAssertion(Means):
    symbol = UNDIRECTED_ASSERTION
    actions = {
        "create": CreateUndirectedAssertion,
        "fork": ForkAssertion,
        "read": ReadAssertion,
        "update": UpdateAssertion,
        "update_members": UpdateUndirectedAssertionMembers,
        "delete": DeleteAssertion
    }

class DirectedAssertion(Means):
    symbol = DIRECTED_ASSERTION
    actions = {
        "create": CreateDirectedAssertion,
        "fork": ForkAssertion,
        "read": ReadAssertion,
        "update": UpdateAssertion,
        "update_members": UpdateDirectedAssertionMembers,
        "delete": DeleteAssertion
    }

class HackMD(Means):
    symbol = HACKMD
    actions = {
        "dereference": DereferenceHackmd,
        "transform": TransformHackmd
    }

class URL(Means):
    symbol = URL
    actions = {
        "dereference": DereferenceUrl,
        "transform": TransformUrl
    }