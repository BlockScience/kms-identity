from ..core import function

@function()
def test_action(rid, context):
    return {
        "data": rid.ref
    }