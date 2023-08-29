from rid_lib.means import *
import api

api.database.drop()

luke = Object.from_string(rid="agent:luke")
luke.observe()

orion = Object.from_string(rid="agent:orion")
orion.observe()

func = Object.from_string(rid="func:gov1")
func.observe()

action1 = Object.from_string(rid="action:1")
action1.observe()

action2 = Object.from_string(rid="action:2")
action2.observe()

working_doc = URL("https://hackmd.io/TBxOcWn_SpWEEcx_t_9GWw?view").transform(means=HackMD.symbol)
working_doc.observe()

assertion = UndirectedAssertion.create({
    "name": "Working Doc",
    "description": "Points to current working doc for identity system development",
    "members": [working_doc.string]
})

# func = DirectedAssertion.create({
#     "name": "Gov Func",
#     "from": [func.string],
#     "to": [action1.string, action2.string]
# })

gov = Governance.create({
    "name": "Working Doc Governance",
    "assertion": assertion.string,
    "agents": [luke.string, orion.string],
})