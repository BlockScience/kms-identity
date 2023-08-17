from rid_lib.core import Action, RID

class TestAction(Action):

    @staticmethod
    def func(rid, context):
        return {
            "data": rid.ref
        }