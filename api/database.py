from api.utils import execute_read, execute_write

@execute_write
def drop(tx):
    DROP = \
        "MATCH (n) DETACH DELETE n"
    tx.run(DROP)

# Object Operations

@execute_write
def create_object(tx, obj):
    CREATE_OBJECT = \
        "CREATE (o:Object) SET o = $props RETURN o AS result"
    
    records = tx.run(CREATE_OBJECT, props=obj)
    result = records.single()
    return result.get("result") if result else None

@execute_read
def read_object(tx, obj_id):
    READ_OBJECT = \
        "MATCH (o:Object {id: $id})-[:REFERS_TO]->(d) RETURN {id: r.id, uri: r.uri, data: properties(d)} AS result"
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

# Relation Operations

@execute_write
def create_set_relation(tx, obj):
    CREATE_SET_RELATION = \
        "CREATE (relation:Set:Relation) SET relation = $props " \
        "WITH relation " \
        "UNWIND $member_ids AS member_id " \
        "MATCH (member) WHERE member.rid = member_id " \
        "CREATE (relation)-[:HAS]->(member) " \
        "RETURN COLLECT(member.rid) AS members"
    
    member_ids = obj.pop("members")
    records = tx.run(CREATE_SET_RELATION, props=obj, member_ids=member_ids)
    result = records.single()
    
    return {
        "rid": obj.get("rid"),
        "members": result.get("members")
    }

@execute_write
def create_directed_relation(tx, obj):
    CREATE_DIRECTED_RELATION = \
        "CREATE (relation:Directed:Relation) SET relation = $props"
        
    CREATE_FROM_EDGES = \
        "MATCH (relation:Directed:Relation) WHERE relation.rid = $relation_id " \
        "UNWIND $from_ids AS from_id " \
        "MATCH (from_node) WHERE from_node.rid = from_id " \
        "CREATE (relation)-[:FROM]->(from_node) " \
        "RETURN COLLECT(from_node.rid) AS from"
        
    CREATE_TO_EDGES = \
        "MATCH (relation:Directed:Relation) WHERE relation.rid = $relation_id " \
        "UNWIND $to_ids AS to_id " \
        "MATCH (to_node) WHERE to_node.rid = to_id " \
        "CREATE (relation)-[:TO]->(to_node) " \
        "RETURN COLLECT(to_node.rid) AS to"         

    relation_id = obj.get("rid")
    from_ids = obj.pop("from")
    to_ids = obj.pop("to")

    tx.run(CREATE_DIRECTED_RELATION, props=obj)
    from_records = tx.run(CREATE_FROM_EDGES, relation_id=relation_id, from_ids=from_ids)
    to_records = tx.run(CREATE_TO_EDGES, relation_id=relation_id, to_ids=to_ids)

    from_result = from_records.single()
    to_result = to_records.single()
    
    return {
        "rid": relation_id,
        "from": from_result.get("from"),
        "to": to_result.get("to")
    }
    
@execute_read
def read_relation(tx, rid):
    READ_RELATION = \
        "MATCH (relation:Relation) WHERE relation.rid = $rid " \
        "RETURN properties(relation) AS relation"
    
    records = tx.run(READ_RELATION, rid=rid)
    result = records.single()

    return result.get("relation")

# Assertion Operations

@execute_write
def create_assertion(tx, obj):
    CREATE_ASSERTION = \
        "CREATE (a:Assertion) SET a = $props " \
        "RETURN a AS result"
    
    records = tx.run(CREATE_ASSERTION, props=obj)
    result = records.single()
    return result.get("result") if result else None
    

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