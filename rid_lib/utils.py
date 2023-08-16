from rid_lib import actions
from rid_lib.exceptions import *

def transform(rid, means):
    available_actions = actions.table.get(rid.means, None)

    if not available_actions:
        raise NoAvailableActionsError(f"No available actions found for '{rid.means}'")
    
    transform_action = available_actions.get("transform", None)

    if not transform_action:
        raise ActionNotFoundError(f"Transform action for '{rid.means}' not found")

    return transform_action.run(rid, context={
        "means": means
    })
    
def dereference(rid):
    available_actions = actions.table.get(rid.means, None)

    if not available_actions: 
        raise NoAvailableActionsError(f"No available action found for means '{rid.means}'")
    
    dereference_action = available_actions.get("dereference", None)

    if not dereference_action:
        raise ActionNotFoundError(f"Reference action for '{rid.means}' not found")
    
    return dereference_action.run(rid)