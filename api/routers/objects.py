from fastapi import APIRouter, HTTPException
from base64 import urlsafe_b64decode
import jsonschema
from jsonschema import ValidationError
from rid_lib.means import RID
from api.utils import pass_exceptions
from api.schema import OBJECT_JSON_ENDPOINT_SCHEMA
from rid_lib.exceptions import *
from rid_lib import utils

router = APIRouter(
    prefix="/object"
)

@router.post("")
@pass_exceptions
def generic_json_endpoint(data: dict):
    try:
        jsonschema.validate(data, OBJECT_JSON_ENDPOINT_SCHEMA)
    except ValidationError as e:
        # print(e.message)
        raise HTTPException(
            status_code=400,
            detail=e.message
        )
    
    rid_str = data["rid"]
    action_str = data["action"]
    context = data.get("context", None)

    rid = utils.parse_rid_string(rid_str)
    result = getattr(rid, action_str)(context)

    if isinstance(result, RID):
        return result.string
    else:
        return result


@router.post("/{rid_str}/{action_str}")
@pass_exceptions
def generic_endpoint(rid_str, action_str, context: dict | None = None, use_base64: bool = False):
    if use_base64:
        rid_bytes = rid_str.encode()
        rid_str = urlsafe_b64decode(rid_bytes).decode()

    rid = utils.parse_rid_string(rid_str)
    result = getattr(rid, action_str)(context)

    if isinstance(result, RID):
        return result.string
    else:
        return result