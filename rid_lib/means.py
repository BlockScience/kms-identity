from .core import RID

class Object(RID):
    symbol = "object"

class UndirectedRelation(RID):
    symbol = "und_rel"

class DirectedRelation(RID):
    symbol = "dir_rel"

class UndirectedAssertion(RID):
    symbol = "und_asrt"

class DirectedAssertion(RID):
    symbol = "dir_asrt"

class URL(Object):
    symbol = "url"

class HackMD(Object):
    symbol = "hackmd"

class Slack(RID):
    symbol = "slack"