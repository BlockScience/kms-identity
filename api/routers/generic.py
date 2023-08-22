from fastapi import APIRouter, HTTPException
from rid_lib import RID, actions
from rid_lib.exceptions import (
    IncompleteRIDError,
    MeansNotFoundError,
    ActionNotFoundError
)

router = APIRouter()

@router.post("/{rid_str}/{action_str}")
def generic_endpoint(rid_str, action_str, context: dict | None = None):
    rid = RID.from_string(rid=rid_str)
    result = getattr(rid, action_str)(context)

    if isinstance(result, RID):
        return result.string
    else:
        return result