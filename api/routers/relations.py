from fastapi import APIRouter
import nanoid
from api import database, utils
from rid_lib import RID
from api.schema import (
    UNDIRECTED_RELATION_SCHEMA,
    DIRECTED_RELATION_SCHEMA
)

router = APIRouter(
    prefix="/relation"
)

@router.post("/undirected")
@utils.validate_json(UNDIRECTED_RELATION_SCHEMA)
def create_undirected_relation(obj: dict):
    rid = RID.from_string(rid="und_rel:" + nanoid.generate())
    return database.create_undirected_relation(rid, obj)

@router.post("/directed")
@utils.validate_json(DIRECTED_RELATION_SCHEMA)
def create_directed_relation(obj: dict):
    rid = RID.from_string(rid="dir_rel:" + nanoid.generate())
    return database.create_directed_relation(rid, obj)

@router.get("/{rid}")
def read_relation(rid: str):
    return database.read_relation(RID.from_string(rid=rid))

@router.delete("/{rid}")
def delete_relation(rid: str):
    database.delete_relation(RID.from_string(rid=rid))