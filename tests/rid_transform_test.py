from rid_lib import RID, utils

rid = RID("url", "https://hackmd.io/uUm16q1oQDmN8T0m9FABNA?view")

new_rid = utils.transform(rid, "hackmd")

print(new_rid)

data = utils.dereference(new_rid)
print(data)