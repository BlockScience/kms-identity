from ..core import function
from ..means import Object
from ..exceptions import *
from .. import table
import api

@function(constructor=True)
def from_string(cls, context):
    rid_str = context["rid"]
    components = rid_str.split(":", 1)

    if len(components) != 2:
        raise IncompleteRIDError
    
    symbol, reference = components

    # matches existing Means class, or creates temporary Object subtype
    try:
        Means = table.lookup(symbol)
    except MeansNotFoundError:
        Means = Object.new_subtype(symbol)

    # Object is a generic Means class that either returns a valid matching Means or generates a temp placeholder
    if cls is Object:
        return Means(reference)
    
    # For all derived means classes, the from_string action will only work if the symbol matches that class (ie 'url:https://google.com' will only be valid when passed into URL.from_string)
    # To input arbitrary RIDs, use Object.from_string
    if cls is Means:
        return cls(reference)
    else:
        raise UnsupportedMeansError(f"The 'from_string' constructor can only be called on '{cls.__name__}' when the RID string uses the '{cls.symbol}' means. To construct arbitrary RID strings, use the generic Object class.")


@function()
def create_object(rid, context):
    api.database.create_object(rid)

    return rid.refresh()
    
@function()
def read_object(rid, context):
    return api.database.read_object(rid)

@function()
def refresh_object(rid, context):
    try:
        data = rid.dereference()
        if data:
            api.database.refresh_object(rid, data)
            return data
        else:
            print("Dereferencing object returned no data")
    except ActionNotFoundError:
        return None