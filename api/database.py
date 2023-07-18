import functools
from api.utils import execute_read, execute_write

# Object Operations

@execute_write
def create_object_reference(tx, obj):
    CREATE_OBJECT_REFERENCE = \
        "CREATE (r:Reference) SET r = $props RETURN r AS result"
    
    records = tx.run(CREATE_OBJECT_REFERENCE, props=obj)
    result = records.single()
    return result.get("result") if result else None

@execute_read
def read_object(tx, obj_id):
    READ_OBJECT = \
        "MATCH (r:Reference {id: $id})-[:REFERS_TO]->(d) RETURN {id: r.id, uri: r.uri, data: properties(d)} AS result"
    records = tx.run(READ_OBJECT, id=obj_id)
    result = records.single()
    return result.get("result") if result else None

@execute_read
def get_object_dereference(tx, obj_id):
    GET_OBJECT_DEREFERENCE = \
        "MATCH (r:Reference {id: $id}) RETURN [r.uri, i.dereference] AS result"
    records = tx.run(GET_OBJECT_DEREFERENCE, id=obj_id)
    result = records.single()
    return result.get("result") if result else None

@execute_write
def refresh_object(tx, obj_id, data):
    REFRESH_OBJECT = \
        "MERGE (r:Reference {id: $id})-[:REFERS_TO]->(d:Data) " \
        "SET d = $props"
    tx.run(REFRESH_OBJECT, id=obj_id, props=data)

# Identity Operations

@execute_write
def create_identity(tx, obj):
    CREATE_IDENTITY = \
        "CREATE (i:Identity) SET i = $props " \
        "RETURN i AS result"
        # "CREATE (i)-[:IS]->(t:Transaction {log: $log})"
    records = tx.run(CREATE_IDENTITY, props=obj)
    result = records.single()
    return result.get("result") if result else None

@execute_read
def read_identity(tx, obj_id):
    READ_IDENTITY = \
        "MATCH (i:Identity {id: $id}) RETURN i AS result"
    records = tx.run(READ_IDENTITY, id=obj_id)
    result = records.single()
    return result.get("result") if result else None

@execute_write
def update_identity(tx, obj_id, obj):
    UPDATE_IDENTITY = \
        "MERGE (i:Identity {id: $id}) SET i += $props RETURN i AS result"
    records = tx.run(UPDATE_IDENTITY, id=obj_id, props=obj)
    result = records.single()
    return result.get("result") if result else None

@execute_write
def delete_identity(tx, obj_id):
    DELETE_IDENTITY = \
        "MERGE (i:Identity {id: $id}) DETACH DELETE i"
    tx.run(DELETE_IDENTITY, id=obj_id)

# @execute_write
# def fork_identity(tx, obj_id):
    
#     FORK_IDENTITY = \
#         "MATCH (:Identity {id: $m_id})-[:IS]->(p:Transaction) " \
#         "CREATE (i:Identity $props)-[:IS]->(n:Transaction {log: $log})-[:SUCCEEDS]->(p)"