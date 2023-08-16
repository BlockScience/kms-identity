import api

api.database.drop()

luke = api.objects.create_object(obj={
    "rid": "user:luke"
})["rid"]

orion = api.objects.create_object(obj={
    "rid": "user:orion"
})["rid"]

func = api.objects.create_object(obj={
    "rid": "func:gov1"
})["rid"]

action1 = api.objects.create_object(obj={
    "rid": "action:1"
})["rid"]

action2 = api.objects.create_object(obj={
    "rid": "action:2"
})["rid"]

working_doc = api.objects.create_object(obj={
    "rid": {
        "reference": "https://hackmd.io/TBxOcWn_SpWEEcx_t_9GWw?view",
        "means": "url"
    },
    "transform": "hackmd"
})["rid"]

assertion = api.assertions.create_undirected_assertion(obj={
    "name": "Working Doc",
    "description": "Points to current working doc for identity system development",
    "members": [working_doc]
})["rid"]

func = api.assertions.create_directed_assertion(obj={
    "name": "Gov Func",
    "from": [func],
    "to": [action1, action2]
})["rid"]

gov = api.assertions.create_directed_assertion(obj={
    "name": "Working Doc Governance",
    "definition": func,
    "from": [luke, orion],
    "to": [assertion]
})