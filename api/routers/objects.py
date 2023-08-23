from fastapi import APIRouter

from api import database, utils
from api.schema import OBJECT_SCHEMA
import rid_lib
from rid_lib import RID

router = APIRouter(
    prefix="/object"
)

@router.post("")
@utils.validate_json(OBJECT_SCHEMA)
def create_object(obj: dict):
    rid_field = obj["rid"]
    transform = obj.get("transform", None)

    if type(rid_field) == str:
        rid_str = rid_field
    elif type(rid_field) == list:
        rid_str = ":".join(rid_field)
    elif type(rid_field) == dict:
        rid_str = f"{rid_field['means']}:{rid_field['reference']}"
    else:
        return "Invalid RID format (this shouldn't happen)"
    
    rid = RID.from_string(rid=rid_str)
    
    if transform:
        rid = rid.transform(means=transform)

    obj = database.create_object(rid)

    try:
        data = rid.dereference()
        if data:
            database.refresh_object(rid, data)
    except Exception as e:
        print(e)

    return obj 

@router.get("/{rid}")
def read_object(rid):
    return database.read_object(RID.from_string(rid))

@router.put("/{rid}")
def update_object(rid):
    rid = RID.from_string(rid)
    data = rid_lib.dereference(rid)
    database.refresh_object(rid, data)
    return data