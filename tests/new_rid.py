from rid_lib.means import *

rid = HackMd("uUm16q1oQDmN8T0m9FABNA")

rel = UndirectedRelation.create(members=[rid.string])


print(rel.read())

print(rel.create(members=[]))

print(UndirectedRelation.read())

rel.delete()