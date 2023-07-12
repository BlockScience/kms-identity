from fastapi import APIRouter, Body, HTTPException, status
import jsonschema, nanoid
from jsonschema.exceptions import ValidationError

from api import database, ingress, utils
from api.schema import IDENTITY_SCHEMA

router = APIRouter(
    prefix="/identity"
)

@router.post("")
@utils.validate_json(IDENTITY_SCHEMA)
def create_identity(identity: dict):
    identity["id"] = nanoid.generate()

    return database.create_identity(identity)

"""
API paths

POST    /identity
GET     /identity/{id}
PUT     /identity/{id}
DELETE  /identity/{id}

        /identity/members
        /identity/{id}/group

"""