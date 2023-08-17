from rid_lib.core import Action, RID

class TestAction(Action):

    @staticmethod
    def func(rid):
        return {
            "data": rid.ref
        }