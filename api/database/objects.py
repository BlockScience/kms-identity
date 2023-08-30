from .utils import execute_read, execute_write, create_object
from rid_lib import RID

# Object Operations

@execute_write
def create(tx, rid: RID):
    create_object(tx, rid)

@execute_write
def refresh(tx, rid: RID, params):
    REFRESH_OBJECT = """
        MERGE (o {rid: $rid})  
        MERGE (o)-[:REFERS_TO]->(d:Data)  
        SET d = $params
        """
    
    tx.run(REFRESH_OBJECT, rid=rid.string, params=params)

@execute_read
def exists(tx, rid: RID):
    OBJECT_EXISTS = """
        MATCH (o {rid: $rid})
        RETURN o
        """
    
    record = tx.run(OBJECT_EXISTS, rid=rid.string)
    return record.single() is not None

@execute_read
def read(tx, rid: RID):
    READ_REFERENT = """
        MATCH (o {rid: $rid})-[:REFERS_TO]->(d)  
        RETURN {rid: o.rid, data: properties(d)} AS result
        """
    
    records = tx.run(READ_REFERENT, rid=rid.string)
    result = records.single()
    if result:
        return result.get("result", None)
