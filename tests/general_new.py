from rid_lib.means import *
import api

api.database.drop()

obj1 = URL("https://hackmd.io/uUm16q1oQDmN8T0m9FABNA?view").transform(means=HackMD.symbol)
obj1.ingress()

obj2 = URL("https://hackmd.io/uUm16q1oQDmN8T0m9FABNA").transform(means=HackMD.symbol)
obj2.ingress()

obj3 = URL("https://hackmd.io/M2IWdXC_S_OSUHA6zkYFYw").transform(means=HackMD.symbol)
obj3.ingress()

obj4 = RID.from_string(rid="test:one")
obj4.ingress()
obj5 = RID.from_string(rid="test:two")
obj5.ingress()

rel1 = UndirectedRelation.create(
    name = "Tag",
    members = [obj1.string, obj2.string, obj3.string]
)

rel2 = DirectedRelation.create({
    "name": "Class Pattern",
    "from": [obj4.string, obj5.string],
    "to": [obj2.string]
})

asr1 = UndirectedAssertion.create(
    name = "Tag",
    members = [obj1.string, obj2.string, obj3.string]
)

asr2 = DirectedAssertion.create({
    "name": "Class Pattern",
    "from": [obj4.string, obj5.string],
    "to": [obj2.string]
})

asr1.update(name="New Name")
asr1.update(name="New Name2")
asr1.update(data="new data")
asr1.update_members(remove=[obj2.string, obj3.string])
asr1.update_members({
    "add": [obj4.string, obj5.string]
})
asr1.update_members({
    "remove": [obj4.string, obj5.string],
    "add": [obj2.string, obj3.string]
})

asr2.update_members({
    "add": {
        "from": [obj2.string],
        "to": [obj4.string, obj5.string]
    },
    "remove": {
        "from": [obj4.string, obj5.string],
        "to": [obj2.string]
    }
})

asr1.fork()
asr2.fork()

print(rel1.read())
print(rel2.read())