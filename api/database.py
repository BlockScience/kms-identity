from api.utils import execute_read, execute_write
from api.queries import *

@execute_write
def drop(tx):
    DROP = \
        "MATCH (n) DETACH DELETE n"
    tx.run(DROP)

# Object Operations

@execute_write
def create_object(tx, rid):
    records = tx.run(CREATE_OBJECT, rid=rid)
    result = records.single()
    return result.get("object") if result else None

@execute_write
def refresh_object(tx, rid, data):
    tx.run(REFRESH_OBJECT, rid=rid, props=data)

@execute_read
def read_object(tx, rid):
    records = tx.run(READ_OBJECT, rid=rid)
    result = records.single()
    return result.get("result") if result else None

# Relation Operations

@execute_write
def create_undirected_relation(tx, obj):
    relation_id = obj.get("rid")
    # removes self edges
    member_rids = [m for m in obj.pop("members") if m != relation_id]

    records = tx.run(CREATE_UNDIRECTED_RELATION, props=obj, member_rids=member_rids)
    result = records.single()
    
    return {
        "rid": obj.get("rid"),
        "members": result.get("members")
    }

@execute_write
def create_directed_relation(tx, obj):
    relation_rid = obj.get("rid")
    # removes self edges
    from_rids = [m for m in obj.pop("from") if m != relation_rid]
    to_rids = [m for m in obj.pop("to") if m != relation_rid]
    
    tx.run(CREATE_DIRECTED_RELATION, props=obj)
    from_records = tx.run(CREATE_FROM_EDGES, rid=relation_rid, from_rids=from_rids)
    to_records = tx.run(CREATE_TO_EDGES, rid=relation_rid, to_rids=to_rids)

    from_result = from_records.single()
    to_result = to_records.single()
    
    return {
        "rid": relation_rid,
        "from": from_result.get("from"),
        "to": to_result.get("to")
    }
    
@execute_read
def read_relation(tx, rid):
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
    tx.run(DELETE_RELATION, rid=rid)

# Assertion Operations

@execute_write
def create_undirected_assertion(tx, obj):
    member_rids = obj.pop("members")
    records = tx.run(CREATE_UNDIRECTED_ASSERTION, props=obj, member_rids=member_rids)
    result = records.single()
    
    return {
        "rid": obj.get("rid"),
        "members": result.get("members")
    }

@execute_write
def create_directed_assertion(tx, obj):     
    assertion_rid = obj.get("rid")
    from_rids = obj.pop("from")
    to_rids = obj.pop("to")

    tx.run(CREATE_DIRECTED_ASSERTION, props=obj)
    from_records = tx.run(CREATE_FROM_EDGES, rid=assertion_rid, from_rids=from_rids)
    to_records = tx.run(CREATE_TO_EDGES, rid=assertion_rid, to_rids=to_rids)

    from_result = from_records.single()
    to_result = to_records.single()
    
    return {
        "rid": assertion_rid,
        "from": from_result.get("from"),
        "to": to_result.get("to")
    }