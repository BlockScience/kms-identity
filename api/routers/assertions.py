from fastapi import APIRouter
import nanoid
from api import database, utils, rid_lib
from api.schema import (
    UNDIRECTED_ASSERTION_SCHEMA,
    DIRECTED_ASSERTION_SCHEMA,
    UPDATE_ASSERTION_SCHEMA,
    UPDATE_UNDIRECTED_ASSERTION_MEMBERS_SCHEMA,
    UPDATE_DIRECTED_ASSERTION_MEMBERS_SCHEMA
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

# The following three endpoints are identical but cover three different paths
@router.put("/{rid}")
@utils.validate_json(UPDATE_ASSERTION_SCHEMA, instance="obj")
def update_assertion(rid: str, obj: dict):
    return database.update_assertion(rid, obj)

@router.put("/undirected/{rid}")
@utils.validate_json(UPDATE_ASSERTION_SCHEMA, instance="obj")
def update_assertion(rid: str, obj: dict):
    return database.update_assertion(rid, obj)

@router.put("/directed/{rid}")
@utils.validate_json(UPDATE_ASSERTION_SCHEMA, instance="obj")
def update_assertion(rid: str, obj: dict):
    return database.update_assertion(rid, obj)

@router.put("/undirected/{rid}/members")
@utils.validate_json(UPDATE_UNDIRECTED_ASSERTION_MEMBERS_SCHEMA, instance="obj")
def update_undirected_assertion_members(rid: str, obj: dict):
    return database.update_undirected_assertion_members(rid, obj)
    print(rid, obj)

@router.put("/directed/{rid}/members")
@utils.validate_json(UPDATE_DIRECTED_ASSERTION_MEMBERS_SCHEMA, instance="obj")
def update_directed_assertion_members(rid: str, obj: dict):
    print(rid, obj)