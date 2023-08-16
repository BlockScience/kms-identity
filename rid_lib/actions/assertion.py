from rid_lib.core import Action, RID
from api.schema import UPDATE_ASSERTION_SCHEMA
import api

class UpdateAssertion(Action):
    needs_context = True
    context_schema = UPDATE_ASSERTION_SCHEMA

    @staticmethod
    def func(rid, context):
        api.database.update_assertion(rid.string, context)