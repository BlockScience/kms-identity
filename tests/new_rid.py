from rid_lib.means import *
import api

api.database.drop()

rid = HackMD("uUm16q1oQDmN8T0m9FABNA")

rel = UndirectedRelation.create(members=[rid.string])
rel2 = UndirectedRelation.create(members=[rid.string])
rel3 = UndirectedRelation.create(members=[rid.string])


print(rel.read())
print(rel2.read())
print(rel3.read())

asrt = UndirectedAssertion.create(name="new assrtion", data="sup", members=[rel.string, rel2.string])
print(asrt.read())

asrt.update(name="new name :)")

asrt.update_members(add=[rel3.string])

asrt2 = DirectedAssertion.create({"from": [rel2.string], "to": [rel.string]}, name="director")

asrt2.update_members(add={"from": [rel3.string]})

# print(rel.create(members=[]))

# print(UndirectedRelation.read())

# rel.delete()