from rid_lib.core import RID

class UndirectedRelation(RID):
    symbol = "und_rel"

class DirectedRelation(RID):
    symbol = "dir_rel"

class UndirectedAssertion(RID):
    symbol = "und_asrt"

class DirectedAssertion(RID):
    symbol = "dir_asrt"

class URL(RID):
    symbol = "url"

class HackMD(RID):
    symbol = "hackmd"

class Slack(RID):
    symbol = "slack"