from rid_lib import actions
from rid_lib.symbols import *
import api

api.database.drop()

obj1 = api.objects.create_object(obj={
        "rid": "url:https://hackmd.io/uUm16q1oQDmN8T0m9FABNA?view",
        "transform": "hackmd"
    })["rid"]

obj2 = api.objects.create_object(obj={
        "rid": ["url", "https://hackmd.io/uUm16q1oQDmN8T0m9FABNA"],
        "transform": "hackmd"
    })["rid"]
obj3 = api.objects.create_object(obj={
        "rid": {
            "means": "url",
            "reference": "https://hackmd.io/M2IWdXC_S_OSUHA6zkYFYw"
        },
        "transform": "hackmd"
    })["rid"]

obj4 = api.objects.create_object(obj={"rid": "test:one"})["rid"]
obj5 = api.objects.create_object(obj={"rid": "test:two"})["rid"]

rel1, _ = actions.lookup(UNDIRECTED_RELATION, "create").run({
    "name": "Tag",
    "members": [obj1, obj2, obj3]
})

rel2, _ = actions.lookup(DIRECTED_RELATION, "create").run({
    "name": "Class Pattern",
    "from": [obj4, obj5],
    "to": [obj2]
})

asr1, _ = actions.lookup(UNDIRECTED_ASSERTION, "create").run({
    "name": "Tag",
    "members": [obj1, obj2, obj3]
})

asr2, _ = actions.lookup(DIRECTED_ASSERTION, "create").run({
    "name": "Class Pattern",
    "from": [obj4, obj5],
    "to": [obj2]
})

actions.lookup(UNDIRECTED_ASSERTION, "update").run(
    asr1, {
    "name": "New Name"
})

actions.lookup(UNDIRECTED_ASSERTION, "update").run(
    asr1, {
    "name": "New Name2"
})

actions.lookup(UNDIRECTED_ASSERTION, "update").run(
    asr1, {
    "data": "new data"
})

actions.lookup(UNDIRECTED_ASSERTION, "update_members").run(
    asr1,
    {
        "remove": [obj2, obj3]
    }
)

actions.lookup(UNDIRECTED_ASSERTION, "update_members").run(
    asr1,
    {
        "add": [obj4, obj5]
    }
)

actions.lookup(UNDIRECTED_ASSERTION, "update_members").run(
    asr1,
    {
        "remove": [obj4, obj5],
        "add": [obj2, obj3]
    }
)

actions.lookup(DIRECTED_ASSERTION, "update_members").run(
    asr2,
    {
        "add": {
            "from": [obj2],
            "to": [obj4, obj5]
        },
        "remove": {
            "from": [obj4, obj5],
            "to": [obj2]
        }
    }
)

actions.lookup(DIRECTED_ASSERTION, "fork").run(asr1)
actions.lookup(UNDIRECTED_ASSERTION, "fork").run(asr2)

rel = actions.lookup(UNDIRECTED_ASSERTION, "read").run(rel1)
print(rel)

rel = actions.lookup(DIRECTED_ASSERTION, "read").run(rel2)
print(rel)

