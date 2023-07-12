import functools
from api.utils import execute_read, execute_write
from api.queries import *

# Object Operations

@execute_write
def create_object_reference(tx, obj):
    records = tx.run(CREATE_OBJECT_REFERENCE, props=obj)
    result = records.single()
    return result.get("result") if result else None

@execute_read
def read_object(tx, obj_id):
    records = tx.run(READ_OBJECT, id=obj_id)
    result = records.single()
    return result.get("result") if result else None

@execute_read
def get_object_dereference(tx, obj_id):
    records = tx.run(GET_OBJECT_DEREFERENCE, id=obj_id)
    result = records.single()
    return result.get("result") if result else None

@execute_write
def refresh_object(tx, obj_id, data):
    tx.run(REFRESH_OBJECT, id=obj_id, props=data)

# Identity Operations

@execute_write
def create_identity(tx, obj):
    records = tx.run(CREATE_IDENTITY, props=obj)
    result = records.single()
    return result.get("result") if result else None

@execute_read
def read_identity(tx, obj_id):
    records = tx.run(READ_IDENTITY, id=obj_id)
    result = records.single()
    return result.get("result") if result else None

@execute_write
def update_identity(tx, obj_id, obj):
    records = tx.run(UPDATE_IDENTITY, id=obj_id, props=obj)
    result = records.single()
    return result.get("result") if result else None

@execute_write
def delete_identity(tx, obj_id):
    tx.run(DELETE_IDENTITY, id=obj_id)