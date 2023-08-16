from rid_lib.core import RID
from rid_lib.actions.assertion import UpdateAssertion


assertion = RID.from_string("asrt:uIJ_3qoSLtVTmjAxeR1xL")

resp = UpdateAssertion.run(assertion, {"name": "New Name"})

print(resp)