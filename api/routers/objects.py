from fastapi import APIRouter, Body
import jsonschema, nanoid
from jsonschema.exceptions import ValidationError

from api.core import driver
from api.schema import OBJECT_REFERENCE_SCHEMA
from api import database

router = APIRouter(
    prefix="/object"
)

@router.get("")
def get_object():
    return "true"

@router.post("")
def create_object(obj: dict = Body(...)):
    try:
        jsonschema.validate(obj, OBJECT_REFERENCE_SCHEMA)
    except ValidationError as e:
        return {"success": False}
    
    obj["id"] = nanoid.generate()

    # database.create_object_reference(obj)

    return {"success": True}