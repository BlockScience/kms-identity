from fastapi import APIRouter
import nanoid
from api import database, utils, rid_lib
from api.schema import (
    UNDIRECTED_ASSERTION_SCHEMA,
    DIRECTED_ASSERTION_SCHEMA,
    UPDATE_ASSERTION_SCHEMA
)

router = APIRouter(
    prefix="/assertion"
)

@router.post("/undirected")
@utils.validate_json(UNDIRECTED_ASSERTION_SCHEMA)
def create_undirected_assertion(obj: dict):
    obj["rid"] = rid_lib.compose("asrt", nanoid.generate())
    return database.create_undirected_assertion(obj)

@router.post("/directed")
@utils.validate_json(DIRECTED_ASSERTION_SCHEMA)
def create_directed_assertion(obj: dict):
    obj["rid"] = rid_lib.compose("asrt", nanoid.generate())
    return database.create_directed_assertion(obj)

@router.put("/{rid}")
@utils.validate_json(UPDATE_ASSERTION_SCHEMA, instance="obj")
def update_assertion(rid: str, obj: dict):
    return database.update_assertion(rid, obj)