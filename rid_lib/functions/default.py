from ..core import function
from ..means import Object
from ..exceptions import *
from .. import table
from api import database

@function(constructor=True, schema={
    "type": "object",
    "properties": {
        "rid": {"type": "string"},
        "observe": {
            "type": "boolean",
            "default": False
        }
    }
})
def from_string(cls, context):
    rid_str = context["rid"]
    observe = context["rid"]
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
        rid = Means(reference)
    
    # For all derived means classes, the from_string action will only work if the symbol matches that class (ie 'url:https://google.com' will only be valid when passed into URL.from_string)
    # To input arbitrary RIDs, use Object.from_string
    elif cls is Means:
        rid = cls(reference)
    else:
        raise UnsupportedMeansError(f"The 'from_string' constructor can only be called on '{cls.__name__}' when the RID string uses the '{cls.symbol}' means. To construct arbitrary RID strings, use the generic Object class.")
    
    if observe:
        rid.observe()

    return rid

@function()
def create_object(rid, context):
    database.objects.create(rid)

    return rid.refresh()

@function()
def object_exists(rid, context):
    return database.objects.exists(rid)
    
@function()
def read_object(rid, context):
    return database.objects.read(rid)

@function()
def refresh_object(rid, context):
    try:
        data = rid.dereference()
        if data:
            database.objects.refresh(rid, data)
            return data
        else:
            print("Dereferencing object returned no data")
    except ActionNotFoundError:
        return None