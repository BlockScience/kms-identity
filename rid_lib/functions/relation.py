from rid_lib.core import Action, Constructor, RID
from rid_lib.symbols import *
from api.schema import *
import api
import nanoid

class CreateUndirectedRelation(Constructor):
    context_schema = UNDIRECTED_RELATION_SCHEMA

    @staticmethod
    def func(context):
        rid = RID(UNDIRECTED_RELATION, nanoid.generate())
        return api.database.create_undirected_relation(rid, context)

class CreateDirectedRelation(Constructor):
    context_schema = DIRECTED_RELATION_SCHEMA

    @staticmethod
    def func(context):
        rid = RID(DIRECTED_RELATION, nanoid.generate())
        return api.database.create_directed_relation(rid, context)
    
class ReadRelation(Action):
    @staticmethod
    def func(rid, context):
        return api.database.read_relation(rid)

class DeleteRelation(Action):
    @staticmethod
    def func(rid, context):
        api.database.delete_assertion(rid)