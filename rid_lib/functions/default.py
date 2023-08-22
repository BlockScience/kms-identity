from ..core import function, RID
from ..exceptions import *
from ..table import lookup
import api

@function(constructor=True)
def from_string(_, context):
    rid_str = context["rid"]
    components = rid_str.split(":", 1)

    if len(components) != 2:
        raise IncompleteRIDError
    
    symbol, reference = components
    RID = lookup(symbol)

    return RID(reference)

@function()
def create_object(rid, context):
    api.database.create_object(rid)
    data = rid.dereference()
    api.database.refresh_object(rid, data)
    return data