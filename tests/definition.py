import api
from rid_lib.means import *

api.database.drop()

definition1 = Object.from_string(rid="url:https://hackmd.io/uUm16q1oQDmN8T0m9FABNA?view").transform(means="hackmd")
definition1.observe()

definition2 = Object.from_string(rid="url:https://hackmd.io/M2IWdXC_S_OSUHA6zkYFYw").transform(means="hackmd")
definition2.observe()

dummy1 = Object.from_string(rid="dummy:1")
dummy1.observe()

dummy2 = Object.from_string(rid="dummy:2")
dummy2.observe()

undirected_rel = UndirectedRelation.create(
    name="Undirected",
    definition=definition1.string,
    members=[dummy2.string]
)

directed_rel = DirectedRelation.create({
    "name": "Directed",
    "definition": definition2.string,
    "from": [dummy1.string],
    "to": [dummy2.string]
})


undirected_asrt = UndirectedAssertion.create({
    "name": "Undirected",
    "definition": None,
    "members": [dummy1.string]
})

directed_asrt = DirectedAssertion.create({
    "name": "Directed",
    "definition": definition2.string,
    "from": [dummy1.string],
    "to": [dummy2.string]
})

undirected_asrt.update_definition(
    definition=definition2.string
)

undirected_asrt.update_definition(
    definition=definition1.string
)

directed_asrt.update_definition(
    definition=None
)
