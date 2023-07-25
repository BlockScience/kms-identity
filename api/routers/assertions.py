from fastapi import APIRouter
import nanoid
from api import database, utils
from api.schema import *

router = APIRouter(
    prefix="/assertion"
)

@router.post("")
@utils.validate_json(ASSERTION_SCHEMA)
def create_assertion(obj: dict):
    obj["rid"] = "internal:" + nanoid.generate()
    return database.create_assertion(obj)