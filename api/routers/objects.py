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
        rid = RID.from_string(rid_field)
    elif type(rid_field) == list:
        rid = RID(*rid_field)
    elif type(rid_field) == dict:
        rid = RID(**rid_field)
    else:
        return "Invalid RID format (this shouldn't happen)"
    
    if transform:
        rid = rid_lib.utils.transform(rid, transform)

    obj = database.create_object(rid.string)

    try:
        data = rid_lib.utils.dereference(rid)
        if data:
            database.refresh_object(rid.string, data)
    except Exception as e:
        print(e)

    return obj 

@router.get("/{rid}")
def read_object(rid):
    return database.read_object(rid)

@router.put("/{rid}")
def update_object(rid):
    data = rid_lib.dereference(rid)
    database.refresh_object(rid, data)
    return data