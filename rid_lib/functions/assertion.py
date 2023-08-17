from rid_lib.core import Action, Constructor, RID
from api.schema import UPDATE_ASSERTION_SCHEMA
import api
import nanoid

class CreateUndirectedAssertion(Constructor):
    @staticmethod
    def func(context):
        rid = RID("und_asrt", nanoid.generate())
        api.database.create_undirected_assertion()

class UpdateAssertion(Action):
    context_schema = UPDATE_ASSERTION_SCHEMA

    @staticmethod
    def func(rid, context):
        api.database.update_assertion(rid.string, context)