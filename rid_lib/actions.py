from .means import *
from .function import *

UndirectedRelation.actions = {
    "create": create_undirected_relation,
    "read": read_relation,
    "delete": delete_relation
}