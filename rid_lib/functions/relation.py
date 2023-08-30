from ..core import function
from api.schema import *
from api import database
import nanoid

@function(constructor=True, schema=UNDIRECTED_RELATION_SCHEMA)
def create_undirected_relation(Means, context):
    rid = Means(nanoid.generate())
    database.relations.create_undirected(rid, context)
    return rid

@function(constructor=True, schema=DIRECTED_RELATION_SCHEMA)
def create_directed_relation(Means, context):
    rid = Means(nanoid.generate())
    database.relations.create_directed(rid, context)
    return rid
    
@function()
def read_undirected_relation(rid, context):
    return database.relations.read_undirected(rid)

@function()
def read_directed_relation(rid, context):
    return database.relations.read_directed(rid)

@function()
def delete_relation(rid, context):
    database.relations.delete(rid)