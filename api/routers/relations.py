from fastapi import APIRouter
import nanoid
from api import database, utils
from api.schema import *

router = APIRouter(
    prefix="/relation"
)

@router.post("")
@utils.validate_json(SET_RELATION_SCHEMA)
def create_set_relation(obj: dict):
    obj["rid"] = "internal:" + nanoid.generate()
    return database.create_set_relation(obj)

@router.post("/directed")
@utils.validate_json(DIRECTED_RELATION_SCHEMA)
def create_directed_relation(obj: dict):
    obj["rid"] = "internal:" + nanoid.generate()
    return database.create_directed_relation(obj)