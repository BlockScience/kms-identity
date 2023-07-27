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

    obj = database.create_object(rid)
    database.refresh_object(rid, data)

    return obj 

@router.get("/{rid}")
def read_object(rid):
    return database.read_object(rid)

@router.put("/{rid}")
def update_object(rid):
    data = rid_lib.dereference(rid)
    database.refresh_object(rid, data)
    return data