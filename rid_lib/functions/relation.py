from ..core import function
from api.schema import *
import api
import nanoid

@function(constructor=True, schema=UNDIRECTED_RELATION_SCHEMA)
def create_undirected_relation(Means, context):
    rid = Means(nanoid.generate())
    api.database.create_undirected_relation(rid, context)
    return rid

@function(constructor=True, schema=DIRECTED_RELATION_SCHEMA)
def create_directed_relation(Means, context):
    rid = Means(nanoid.generate())
    api.database.create_directed_relation(rid, context)
    return rid
    
@function()
def read_undirected_relation(rid, context):
    return api.database.read_undirected_relation(rid)

@function()
def read_directed_relation(rid, context):
    return api.database.read_directed_relation(rid)

@function()
def delete_relation(rid, context):
    api.database.delete_relation(rid)