from ..core import function
from api.schema import *
import api
import nanoid

@function(constructor=True, schema=UNDIRECTED_ASSERTION_SCHEMA)
def create_undirected_assertion(RID, context):
    rid = RID(nanoid.generate())
    api.database.create_undirected_assertion(rid, context)
    return rid

@function(constructor=True, schema=DIRECTED_ASSERTION_SCHEMA)
def create_directed_assertion(RID, context):
    rid = RID(nanoid.generate())
    api.database.create_directed_assertion(rid, context)
    return rid

@function()
def fork_assertion(rid, context):
    RID = rid.means
    new_rid = RID(nanoid.generate())
    api.database.fork_assertion(rid, new_rid)
    return new_rid

@function()
def read_assertion(rid, context):
    return api.database.read_relation(rid)

@function(schema=UPDATE_ASSERTION_SCHEMA)
def update_assertion(rid, context):
    api.database.update_assertion(rid, context)

@function(schema=UPDATE_UNDIRECTED_ASSERTION_MEMBERS_SCHEMA)
def update_undirected_assertion_members(rid, context):
    api.database.update_undirected_assertion_members(rid, context)

@function(schema=UPDATE_DIRECTED_ASSERTION_MEMBERS_SCHEMA)
def update_directed_assertion_members(rid, context):
    api.database.update_directed_assertion_members(rid, context)

@function()
def delete_assertion(rid, context):
    api.database.delete_assertion(rid)