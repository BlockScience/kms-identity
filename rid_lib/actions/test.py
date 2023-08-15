from rid_lib.core import Action, RID

class TestAction(Action):
    supported_means=["test"]

    @staticmethod
    def func(rid):
        return {
            "data": rid.ref
        }
    
table = {
    "dereference": TestAction
}