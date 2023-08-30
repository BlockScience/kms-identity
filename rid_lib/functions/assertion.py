from ..core import function
from api.schema import *
from api import database
import nanoid

@function(constructor=True, schema=UNDIRECTED_ASSERTION_SCHEMA)
def create_undirected_assertion(Means, context):
    if "reference" in context:
        reference = context["reference"]
    else:
        reference = nanoid.generate()

    rid = Means(reference)

    database.assertions.create_undirected(rid, context)
    return rid

@function(constructor=True, schema=DIRECTED_ASSERTION_SCHEMA)
def create_directed_assertion(Means, context):
    if "reference" in context:
        reference = context["reference"]
    else:
        reference = nanoid.generate()
        
    rid = Means(reference)
    database.assertions.create_directed(rid, context)
    return rid

@function()
def fork_assertion(rid, context):
    Means = rid.means
    new_rid = Means(nanoid.generate())
    database.assertions.fork(rid, new_rid)
    return new_rid

@function()
def read_transactions(rid, context):
    return database.assertions.read_transactions(rid)

@function(schema=UPDATE_ASSERTION_SCHEMA)
def update_assertion(rid, context):
    database.assertions.update(rid, context)

@function(schema=UPDATE_ASSERTION_DEFINITION_SCHEMA)
def update_assertion_definition(rid, context):
    database.assertions.update_definition(rid, context)

@function(schema=UPDATE_UNDIRECTED_ASSERTION_MEMBERS_SCHEMA)
def update_undirected_assertion_members(rid, context):
    database.assertions.update_undirected_members(rid, context)

@function(schema=UPDATE_DIRECTED_ASSERTION_MEMBERS_SCHEMA)
def update_directed_assertion_members(rid, context):
    database.assertions.update_directed_members(rid, context)

@function()
def delete_assertion(rid, context):
    database.assertions.delete(rid)