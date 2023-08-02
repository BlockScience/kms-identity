import api

api.database.drop()

obj1 = api.objects.create_object(obj={"transform": {
        "reference": "https://hackmd.io/uUm16q1oQDmN8T0m9FABNA?view",
        "from": "url",
        "to": "hackmd"
    }})["rid"]
obj2 = api.objects.create_object(obj={"transform": {
        "reference": "https://hackmd.io/uUm16q1oQDmN8T0m9FABNA",
        "from": "url",
        "to": "hackmd"
    }})["rid"]
obj3 = api.objects.create_object(obj={"transform": {
        "reference": "https://hackmd.io/M2IWdXC_S_OSUHA6zkYFYw",
        "from": "url",
        "to": "hackmd"
    }})["rid"]

obj4 = api.objects.create_object(obj={"rid": "test:one"})["rid"]
obj5 = api.objects.create_object(obj={"rid": "test:two"})["rid"]


rel1 = api.relations.create_undirected_relation(obj={
    "name": "Tag",
    "members": [obj1, obj2, obj3]
})["rid"]

rel2 = api.relations.create_directed_relation(obj={
    "name": "Class Pattern",
    "from": [obj4, obj5],
    "to": [obj2]
})["rid"]

asr1 = api.assertions.create_undirected_assertion(obj={
    "name": "Tag",
    "members": [obj1, obj2, obj3]
})["rid"]

asr2 = api.assertions.create_directed_assertion(obj={
    "name": "Class Pattern",
    "from": [obj4, obj5],
    "to": [obj2]
})["rid"]

api.assertions.update_assertion(rid=asr1, obj={"name": "New Name"})
api.assertions.update_assertion(rid=asr1, obj={"name": "New Name2"})
api.assertions.update_assertion(rid=asr1, obj={"data": "new data"})

# api.assertions.update_undirected_assertion_members(rid=asr1, obj={
#     "remove": [obj2, obj3]
# })

# api.assertions.update_undirected_assertion_members(rid=asr1, obj={
#     "add": [obj4, obj5]
# })

# api.assertions.update_undirected_assertion_members(rid=asr1, obj={
#     "remove": [obj4, obj5],
#     "add": [obj2, obj3]
# })

# api.assertions.delete_assertion(rid=asr1)

api.assertions.update_directed_assertion_members(rid=asr2, obj={
    "add": {
        "from": [obj2],
        "to": [obj4, obj5]
    },
    "remove": {
        "from": [obj4, obj5],
        "to": [obj2]
    }
})

api.assertions.fork_assertion(forked_rid=asr1)

rel = api.relations.read_relation(rel1)
print(rel)

rel = api.relations.read_relation(rel2)
print(rel)