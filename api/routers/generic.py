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
    try:
        rid = RID.from_string(rid_str)
        means = rid.means
    except IncompleteRIDError:
        means = rid
    
    try:
        action = actions.lookup(means, action_str)
    except (MeansNotFoundError, ActionNotFoundError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    result = action.run(rid, context)

    if type(result) == RID:
        return result.string
    else:
        return result