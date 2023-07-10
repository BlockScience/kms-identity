from fastapi import APIRouter, Body
import jsonschema, nanoid
from jsonschema.exceptions import ValidationError

from api.core import driver
from api.utils import new_transaction, run_transaction
from api.schema import OBJECT_REFERENCE_SCHEMA
from api.queries import CREATE_OBJECT_REFERENCE
from api.transactions import create_object_reference

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
        return
    
    obj["id"] = nanoid.generate()

    print('Yo')
    
    with driver.session(database="neo4j") as session:
        session.execute_write(create_object_reference, obj)


    return {"success": True}