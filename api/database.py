from api.utils import execute_read, execute_write

@execute_write
def drop(tx):
    DROP = \
        "MATCH (n) DETACH DELETE n"
    tx.run(DROP)

# Object Operations

@execute_write
def create_object(tx, obj_id):
    CREATE_OBJECT = \
        "MERGE (object:Object {rid: $obj_id}) RETURN object"
    
    records = tx.run(CREATE_OBJECT, obj_id=obj_id)
    result = records.single()
    return result.get("object") if result else None

@execute_write
def refresh_object(tx, obj_id, data):
    REFRESH_OBJECT = \
        "MERGE (o:Object {rid: $obj_id}) " \
        "MERGE (o)-[:REFERS_TO]->(d:Data) " \
        "SET d = $props"
    tx.run(REFRESH_OBJECT, obj_id=obj_id, props=data)

@execute_read
def read_object(tx, obj_id):
    READ_OBJECT = \
        "MATCH (o:Object {rid: $obj_id})-[:REFERS_TO]->(d) " \
        "RETURN {rid: o.rid, data: properties(d)} AS result"
    records = tx.run(READ_OBJECT, obj_id=obj_id)
    result = records.single()
    return result.get("result") if result else None

# Relation Operations

@execute_write
def create_undirected_relation(tx, obj):
    CREATE_UNDIRECTED_RELATION = \
        "CREATE (relation:Undirected:Relation) SET relation = $props " \
        "WITH relation " \
        "UNWIND $member_ids AS member_id " \
        "MATCH (member) WHERE member.rid = member_id " \
        "CREATE (relation)-[:HAS]->(member) " \
        "RETURN COLLECT(member.rid) AS members"
    
    relation_id = obj.get("rid")
    # removes self edges
    member_ids = [m for m in obj.pop("members") if m != relation_id]

    records = tx.run(CREATE_UNDIRECTED_RELATION, props=obj, member_ids=member_ids)
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
    # removes self edges
    from_ids = [m for m in obj.pop("from") if m != relation_id]
    to_ids = [m for m in obj.pop("to") if m != relation_id]
    
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
        "MATCH (relation:Relation) " \
        "WHERE relation.rid = $rid " \
        "RETURN relation"
    
    READ_UNDIRECTED_RELATION = \
        "MATCH (relation:Undirected:Relation)-[:HAS]->(object) " \
        "WHERE relation.rid = $rid " \
        "RETURN object.rid AS object"
    
    READ_DIRECTED_RELATION = \
        "MATCH (relation:Directed:Relation)-[e:TO|FROM]->(object) " \
        "WHERE relation.rid = $rid " \
        "RETURN type(e) AS type, object.rid AS object"
    
    records = tx.run(READ_RELATION, rid=rid)
    result = records.single()

    if not result:
        return None
    
    relation = result.get("relation")

    if "Undirected" in relation.labels:
        member_records = tx.run(READ_UNDIRECTED_RELATION, rid=rid)
        objects = []

        for record in member_records:
            rid = record.get("object")
            objects.append(rid)

        return {
            **relation._properties,
            "type": "undirected",
            "members": objects
        }

    elif "Directed" in relation.labels:
        member_records = tx.run(READ_DIRECTED_RELATION, rid=rid)
        from_objects = []
        to_objects = []

        for record in member_records:
            rid = record.get("object")
            direction = record.get("type")

            if direction == "FROM":
                from_objects.append(rid)
            elif direction == "TO":
                to_objects.append(rid)

        return {
            **relation._properties,
            "type": "directed",
            "from": from_objects,
            "to": to_objects
        }
    
@execute_write
def delete_relation(tx, rid):
    DELETE_RELATION = \
        "MATCH (relation:Relation) " \
        "WHERE relation.rid = $rid " \
        "DETACH DELETE relation"
    
    tx.run(DELETE_RELATION, rid=rid)

# Assertion Operations

@execute_write
def create_undirected_assertion(tx, obj):
    CREATE_UNDIRECTED_ASSERTION = \
        "CREATE (assertion:Undirected:Assertion) SET assertion = $props " \
        "WITH assertion " \
        "UNWIND $member_ids AS member_id " \
        "MATCH (member) WHERE member.rid = member_id " \
        "CREATE (assertion)-[:HAS]->(member) " \
        "RETURN COLLECT(member.rid) AS members"
    
    member_ids = obj.pop("members")
    records = tx.run(CREATE_UNDIRECTED_ASSERTION, props=obj, member_ids=member_ids)
    result = records.single()
    
    return {
        "rid": obj.get("rid"),
        "members": result.get("members")
    }

@execute_write
def create_directed_assertion(tx, obj):
    CREATE_DIRECTED_ASSERTION = \
        "CREATE (assertion:Directed:Assertion) SET assertion = $props"
        
    CREATE_FROM_EDGES = \
        "MATCH (assertion:Directed:Assertion) WHERE assertion.rid = $assertion_id " \
        "UNWIND $from_ids AS from_id " \
        "MATCH (from_node) WHERE from_node.rid = from_id " \
        "CREATE (assertion)-[:FROM]->(from_node) " \
        "RETURN COLLECT(from_node.rid) AS from"
        
    CREATE_TO_EDGES = \
        "MATCH (assertion:Directed:Assertion) WHERE assertion.rid = $assertion_id " \
        "UNWIND $to_ids AS to_id " \
        "MATCH (to_node) WHERE to_node.rid = to_id " \
        "CREATE (assertion)-[:TO]->(to_node) " \
        "RETURN COLLECT(to_node.rid) AS to"         

    assertion_id = obj.get("rid")
    from_ids = obj.pop("from")
    to_ids = obj.pop("to")

    tx.run(CREATE_DIRECTED_ASSERTION, props=obj)
    from_records = tx.run(CREATE_FROM_EDGES, assertion_id=assertion_id, from_ids=from_ids)
    to_records = tx.run(CREATE_TO_EDGES, assertion_id=assertion_id, to_ids=to_ids)

    from_result = from_records.single()
    to_result = to_records.single()
    
    return {
        "rid": assertion_id,
        "from": from_result.get("from"),
        "to": to_result.get("to")
    }