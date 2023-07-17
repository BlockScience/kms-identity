from fastapi import APIRouter, Body, HTTPException, status
import jsonschema, nanoid
from jsonschema.exceptions import ValidationError

from api import database, utils
from api.schema import IDENTITY_SCHEMA, UPDATE_IDENTITY_SCHEMA

router = APIRouter(
    prefix="/identity"
)

@router.post("")
@utils.validate_json(IDENTITY_SCHEMA)
def create_identity(obj: dict):
    obj["id"] = nanoid.generate()
    return database.create_identity(obj)

@router.get("/{obj_id}")
def read_identity(obj_id: str):
    return database.read_identity(obj_id)

@router.put("/{obj_id}")
@utils.validate_json(UPDATE_IDENTITY_SCHEMA, instance="obj")
def update_identity(obj: dict, obj_id: str):
    return database.update_identity(obj_id, obj)

@router.delete("/{obj_id}")
def delete_identity(obj_id: str):
    database.delete_identity(obj_id)

"""
API paths

POST    /identity
GET     /identity/{id}
PUT     /identity/{id}
DELETE  /identity/{id}

        /identity/members
        /identity/{id}/group

"""