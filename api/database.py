import functools
from api.utils import execute_read, execute_write
from api.queries import *

@execute_write
def create_object_reference(tx, obj):
    result = tx.run(CREATE_OBJECT_REFERENCE, props=obj)
    return list(result)