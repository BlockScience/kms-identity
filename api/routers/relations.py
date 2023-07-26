from fastapi import APIRouter
import nanoid
from api import database, utils
from api.schema import *

router = APIRouter(
    prefix="/relation"
)

@router.post("/undirected")
@utils.validate_json(UNDIRECTED_RELATION_SCHEMA)
def create_undirected_relation(obj: dict):
    obj["rid"] = "internal:" + nanoid.generate()
    return database.create_undirected_relation(obj)

@router.post("/directed")
@utils.validate_json(DIRECTED_RELATION_SCHEMA)
def create_directed_relation(obj: dict):
    obj["rid"] = "internal:" + nanoid.generate()
    return database.create_directed_relation(obj)

@router.get("/{rid}")
def read_relation(rid: str):
    return database.read_relation(rid)

@router.delete("/{rid}")
def delete_relation(rid: str):
    database.delete_relation(rid)