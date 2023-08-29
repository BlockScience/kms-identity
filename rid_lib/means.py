from .core import RID

class Object(RID):
    symbol = "object"

class UndirectedRelation(Object):
    symbol = "und_rel"

class DirectedRelation(Object):
    symbol = "dir_rel"

class UndirectedAssertion(Object):
    symbol = "und_asrt"

class DirectedAssertion(Object):
    symbol = "dir_asrt"

class Agent(UndirectedAssertion):
    symbol = "agent"

class Governance(DirectedAssertion):
    symbol = "gov"

class Belief(DirectedAssertion):
    symbol = "belief"

class URL(Object):
    symbol = "url"

class HackMD(Object):
    symbol = "hackmd"

class Slack(Object):
    symbol = "slack"