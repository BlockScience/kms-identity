from rid_lib import actions
from rid_lib.exceptions import *

def transform(rid, means):
    action = actions.lookup(rid.means, "transform")
    return action.run(rid, context={
        "means": means
    })
    
def dereference(rid):
    action = actions.lookup(rid.means, "dereference")
    return action.run(rid)