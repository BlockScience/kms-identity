from fastapi import APIRouter, Body, HTTPException, status
import jsonschema, nanoid
from jsonschema.exceptions import ValidationError

from api import database, utils
from api.schema import OBJECT_SCHEMA
from api import rid_lib

router = APIRouter(
    prefix="/object"
)

@router.post("")
@utils.validate_json(OBJECT_SCHEMA)
def create_object(obj: dict):
    if "rid" in obj:
        rid = obj["rid"]
    else:
        transform = obj["transform"]
        rid = rid_lib.transform(
            transform["reference"],
            from_=transform["from"], 
            to=transform["to"]
        )

    data = rid_lib.dereference(rid)

    return data
    # return database.create_object(obj)

@router.get("/{obj_id}")
def read_object(obj_id):
    return database.read_object(obj_id)

# @router.put("/{obj_id}")
# def update_object(obj_id):
#     uri, deref_func = database.get_object_dereference(obj_id)
#     dereference = getattr(dereferencers, deref_func)
#     data = dereference(uri)
#     database.refresh_object(obj_id, data)
#     return data