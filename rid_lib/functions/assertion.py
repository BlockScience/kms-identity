from rid_lib.core import Action, Constructor, RID
from rid_lib.symbols import *
from api.schema import *
import api
import nanoid

class CreateUndirectedAssertion(Constructor):
    context_schema = UNDIRECTED_ASSERTION_SCHEMA

    @staticmethod
    def func(context):
        rid = RID(UNDIRECTED_ASSERTION, nanoid.generate())
        return api.database.create_undirected_assertion(rid, context)

class CreateDirectedAssertion(Constructor):
    context_schema = DIRECTED_ASSERTION_SCHEMA

    @staticmethod
    def func(context):
        rid = RID(DIRECTED_ASSERTION, nanoid.generate())
        return api.database.create_directed_assertion(rid, context)
    
class ForkAssertion(Action):
    @staticmethod
    def func(rid, context):
        new_rid = RID(rid.means, nanoid.generate())
        return api.database.fork_assertion(rid, new_rid)

class ReadAssertion(Action):
    @staticmethod
    def func(rid, context):
        return api.database.read_relation(rid)

class UpdateAssertion(Action):
    context_schema = UPDATE_ASSERTION_SCHEMA

    @staticmethod
    def func(rid, context):
        api.database.update_assertion(rid, context)

class UpdateUndirectedAssertionMembers(Action):
    context_schema = UPDATE_UNDIRECTED_ASSERTION_MEMBERS_SCHEMA

    @staticmethod
    def func(rid, context):
        api.database.update_undirected_assertion_members(rid, context)

class UpdateDirectedAssertionMembers(Action):
    context_schema = UPDATE_DIRECTED_ASSERTION_MEMBERS_SCHEMA

    @staticmethod
    def func(rid, context):
        api.database.update_directed_assertion_members(rid, context)

class DeleteAssertion(Action):
    @staticmethod
    def func(rid, context):
        api.database.delete_assertion(rid)