from rid_lib.core import Means
from rid_lib.functions import *

class Assertion(Means):
    symbol = "asrt"
    actions = {
        "update": UpdateAssertion
    }

class HackMD(Means):
    symbol = "hackmd"
    actions = {
        "dereference": DereferenceHackmd,
        "transform": TransformHackmd
    }

class URL(Means):
    symbol = "url"
    actions = {
        "dereference": DereferenceUrl,
        "transform": TransformUrl
    }