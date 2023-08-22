from rid_lib.core import RID

class UndirectedRelation(RID):
    symbol = "und_rel"

class DirectedRelation(RID):
    symbol = "dir_rel"

class UndirectedAssertion(RID):
    symbol = "und_asrt"

class DirectedAssertion(RID):
    symbol = "dir_asrt"

class HackMd(RID):
    symbol = "hackmd"

class Url(RID):
    symbol = "url"