from .core import function
from api.schema import *
import nanoid
import api

@function(schema=UNDIRECTED_RELATION_SCHEMA)
def create_undirected_relation(Means, context):
    rid = Means(nanoid.generate())
    api.database.create_undirected_relation(rid, context)
    return rid

@function()
def read_relation(rid, context):
    return api.database.read_relation(rid)

@function()
def delete_relation(rid, context):
    api.database.delete_relation(rid)