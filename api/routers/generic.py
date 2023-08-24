from fastapi import APIRouter, HTTPException
from base64 import urlsafe_b64decode
from rid_lib.means import RID,Object
from api.utils import pass_exceptions
from rid_lib.exceptions import *
from rid_lib import table

router = APIRouter()

@router.post("/{rid_str}/{action_str}")
@pass_exceptions
def generic_endpoint(rid_str, action_str, context: dict | None = None, use_base64: bool = False):
    if use_base64:
        rid_bytes = rid_str.encode()
        rid_str = urlsafe_b64decode(rid_bytes).decode()

    components = rid_str.split(":", 1)
    reference = None

    if len(components) == 0:
        raise IncompleteRIDError
    elif len(components) == 1:
        symbol, = components
    elif len(components) == 2:
        symbol, reference = components

    Means = table.lookup(symbol)

    if reference:
        rid = Means(reference)
        result = getattr(rid, action_str)(context)
    else:
        result = getattr(Means, action_str)(context)

    if isinstance(result, RID):
        return result.string
    else:
        return result