from ..core import function
from ..exceptions import *
from ..table import lookup

@function(constructor=True)
def from_string(_, context):
    rid_str = context["rid"]
    components = rid_str.split(":", 1)

    if len(components) != 2:
        raise IncompleteRIDError
    
    symbol, reference = components
    RID = lookup(symbol)

    return RID(reference)