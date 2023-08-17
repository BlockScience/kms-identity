from rid_lib.core import RID
from rid_lib.functions.assertion import UpdateAssertion


assertion = RID.from_string("asrt:HsSLHzsNcYy2Wahi_TFs8")

resp = UpdateAssertion.run(assertion, {"name": "New Name"})

print(resp)