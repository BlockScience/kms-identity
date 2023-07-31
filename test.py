import api

api.database.drop()

obj1 = api.objects.create_object(obj={"transform": {
        "reference": "https://hackmd.io/uUm16q1oQDmN8T0m9FABNA?view",
        "from": "url",
        "to": "hackmd"
    }})
obj2 = api.objects.create_object(obj={"transform": {
        "reference": "https://hackmd.io/uUm16q1oQDmN8T0m9FABNA",
        "from": "url",
        "to": "hackmd"
    }})
obj3 = api.objects.create_object(obj={"transform": {
        "reference": "https://hackmd.io/M2IWdXC_S_OSUHA6zkYFYw",
        "from": "url",
        "to": "hackmd"
    }})

obj4 = api.objects.create_object(obj={"rid": "test:one"})
obj5 = api.objects.create_object(obj={"rid": "test:two"})


rel1 = api.relations.create_undirected_relation(obj={
    "name": "Tag",
    "members": [obj1["rid"], obj2["rid"], obj3["rid"]]
})

rel2 = api.relations.create_directed_relation(obj={
    "name": "Class Pattern",
    "from": [obj4["rid"], obj5["rid"]],
    "to": [obj2["rid"]]
})

asr1 = api.assertions.create_undirected_assertion(obj={
    "name": "Tag",
    "members": [obj1["rid"], obj2["rid"], obj3["rid"]]
})

asr2 = api.assertions.create_directed_assertion(obj={
    "name": "Class Pattern",
    "from": [obj4["rid"], obj5["rid"]],
    "to": [obj2["rid"]]
})

api.assertions.update_assertion(rid=asr1["rid"], obj={"name": "New Name"})
api.assertions.update_assertion(rid=asr1["rid"], obj={"name": "New Name2"})
api.assertions.update_assertion(rid=asr1["rid"], obj={"data": "new data"})


rel = api.relations.read_relation(rel1["rid"])
print(rel)

rel = api.relations.read_relation(rel2["rid"])
print(rel)