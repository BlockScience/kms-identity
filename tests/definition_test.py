import api

api.database.drop()

definition = api.objects.create_object(obj={"transform": {
        "reference": "https://hackmd.io/uUm16q1oQDmN8T0m9FABNA?view",
        "from": "url",
        "to": "hackmd"
    }})["rid"]

dummy1 = api.objects.create_object(obj={
    "rid": "dummy:1"
})["rid"]

dummy2 = api.objects.create_object(obj={
    "rid": "dummy:2"
})["rid"]

undirected = api.relations.create_undirected_relation(obj={
    "name": "Undirected",
    "definition": definition,
    "members": [dummy1, dummy2]
})["rid"]

directed = api.relations.create_directed_relation(obj={
    "name": "Directed",
    "definition": definition,
    "from": [dummy1],
    "to": [dummy2]
})["rid"]