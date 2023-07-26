from fastapi import APIRouter, Body, HTTPException, status
import jsonschema, nanoid
from jsonschema.exceptions import ValidationError

from api import database, utils
from api.schema import OBJECT_SCHEMA

router = APIRouter(
    prefix="/object"
)

@router.post("")
@utils.validate_json(OBJECT_SCHEMA)
def create_object(obj: dict):
    return database.create_object(obj)

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