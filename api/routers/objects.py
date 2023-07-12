from fastapi import APIRouter, Body
import jsonschema, nanoid
from jsonschema.exceptions import ValidationError

from api.core import driver
from api.schema import OBJECT_REFERENCE_SCHEMA
from api import database, ingress

router = APIRouter(
    prefix="/object"
)

@router.post("")
def create_object(obj: dict = Body(...)):
    try:
        jsonschema.validate(obj, OBJECT_REFERENCE_SCHEMA)
    except ValidationError as e:
        return {"success": False}
    
    obj["id"] = nanoid.generate()

    database.create_object_reference(obj)

    return {"success": True}

@router.get("/{obj_id}")
def read_object(obj_id):
    print('test')
    return database.read_object(obj_id)

@router.put("/{obj_id}")
def update_object(obj_id):
    uri, deref_func = database.get_object_dereference(obj_id)
    dereference = getattr(ingress, deref_func)
    data = dereference(uri)
    database.refresh_object(obj_id, data)
    return data