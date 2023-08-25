from . import table
from .means import Object
from .exceptions import *

def parse_rid_string(rid_str):
    components = rid_str.split(":", 1)
    reference = None

    if len(components) == 0:
        raise IncompleteRIDError
    elif len(components) == 1:
        symbol, = components
    elif len(components) == 2:
        symbol, reference = components

    try:    
        Means = table.lookup(symbol)
    except MeansNotFoundError:
        Means = Object.new_subtype(symbol)

    if reference:
        return Means(reference)
    else:
        return Means
