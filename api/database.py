import functools
from api.utils import execute_read, execute_write
from api.queries import *

@execute_write
def create_object_reference(tx, obj):
    records = tx.run(CREATE_OBJECT_REFERENCE, props=obj)
    return records.single().get("result", None)

@execute_read
def read_object(tx, obj_id):
    records = tx.run(READ_OBJECT)
    return [obj.get('result') for obj in records]

@execute_read
def get_object_dereference(tx, obj_id):
    records = tx.run(GET_OBJECT_DEREFERENCE, id=obj_id)
    return records.single().get('result', None)

@execute_write
def refresh_object(tx, obj_id, data):
    tx.run(REFRESH_OBJECT, id=obj_id, props=data)

@execute_write
def create_identity(tx, identity):
    records = tx.run(CREATE_IDENTITY, props=identity)
    return records.single().get("result", None)