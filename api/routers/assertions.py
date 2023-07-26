from fastapi import APIRouter
import nanoid
from api import database, utils
from api.schema import (
    UNDIRECTED_ASSERTION_SCHEMA,
    DIRECTED_ASSERTION_SCHEMA
)

router = APIRouter(
    prefix="/assertion"
)

@router.post("/undirected")
@utils.validate_json(UNDIRECTED_ASSERTION_SCHEMA)
def create_assertion(obj: dict):
    obj["rid"] = "asrt" + nanoid.generate()
    return database.create_undirected_assertion(obj)

@router.post("/directed")
@utils.validate_json(DIRECTED_ASSERTION_SCHEMA)
def create_assertion(obj: dict):
    obj["rid"] = "asrt" + nanoid.generate()
    return database.create_directed_assertion(obj)