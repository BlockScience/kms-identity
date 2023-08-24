from fastapi import APIRouter, HTTPException
from base64 import urlsafe_b64decode
from rid_lib.means import RID,Object
from api.utils import pass_exceptions

router = APIRouter()

@router.post("/{rid_str}/{action_str}")
@pass_exceptions
def generic_endpoint(rid_str, action_str, context: dict | None = None, use_base64: bool = False):
    if use_base64:
        rid_bytes = rid_str.encode()
        rid_str = urlsafe_b64decode(rid_bytes).decode()

    rid = Object.from_string(rid=rid_str)

    result = getattr(rid, action_str)(context)

    if isinstance(result, RID):
        return result.string
    else:
        return result