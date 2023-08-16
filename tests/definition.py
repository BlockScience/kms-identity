import api

api.database.drop()

definition1 = api.objects.create_object(obj={
        "rid": "url:https://hackmd.io/uUm16q1oQDmN8T0m9FABNA?view",
        "transform": "hackmd"
    })["rid"]

definition2 = api.objects.create_object(obj={
        "rid": "url:https://hackmd.io/M2IWdXC_S_OSUHA6zkYFYw",
        "transform": "hackmd"
    })["rid"]

dummy1 = api.objects.create_object(obj={
    "rid": "dummy:1"
})["rid"]

dummy2 = api.objects.create_object(obj={
    "rid": "dummy:2"
})["rid"]

undirected_rel = api.relations.create_undirected_relation(obj={
    "name": "Undirected",
    "definition": definition1,
    "members": [dummy2]
})["rid"]

directed_rel = api.relations.create_directed_relation(obj={
    "name": "Directed",
    "definition": definition2,
    "from": [dummy1],
    "to": [dummy2]
})["rid"]

undirected_rel = api.assertions.create_undirected_assertion(obj={
    "name": "Undirected",
    "definition": None,
    "members": [dummy1]
})["rid"]

directed_rel = api.assertions.create_directed_assertion(obj={
    "name": "Directed",
    "definition": definition2,
    "from": [dummy1],
    "to": [dummy2]
})["rid"]

api.assertions.update_assertion_definition(undirected_rel, obj={
    "definition": definition2
})

api.assertions.update_assertion_definition(undirected_rel, obj={
    "definition": definition1
})

api.assertions.update_assertion_definition(directed_rel, obj={
    "definition": None
})