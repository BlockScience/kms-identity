from .utils import *
from rid_lib import RID

# Relation Operations

@execute_write
def create_undirected(tx, rid: RID, params):
    # removes self edges
    member_rids = [m for m in params.pop("members", []) if m != rid.string]
    definition_rid = params.pop("definition", None)

    create_object(tx, rid, params)
    create_edges(tx, rid, "HAS", member_rids)

    if definition_rid and (definition_rid != rid.string):
        set_definition(tx, rid, definition_rid)

@execute_write
def create_directed(tx, rid: RID, params):
    # removes self edges
    from_rids = [m for m in params.pop("from", []) if m != rid.string]
    to_rids = [m for m in params.pop("to", []) if m != rid.string]
    definition_rid = params.pop("definition", None)

    create_object(tx, rid, params)
    create_edges(tx, rid, "FROM", from_rids)
    create_edges(tx, rid, "TO", to_rids)

    if definition_rid and (definition_rid != rid.string):
        set_definition(tx, rid, definition_rid)

    
@execute_read
def read_undirected(tx, rid: RID):
    READ_UNDIRECTED_RELATION = """
        MATCH (relation)-[:HAS]->(object)  
        WHERE relation.rid = $rid  
        RETURN object.rid AS object
        """
    
    obj = read_object(tx, rid)

    member_records = tx.run(READ_UNDIRECTED_RELATION, rid=rid.string)
    members = []

    for record in member_records:
        rid = record.get("object")
        members.append(rid)

    return {
        **obj._properties,
        "members": members
    }

@execute_read
def read_directed(tx, rid: RID):
    READ_DIRECTED_RELATION = """
        MATCH (relation)-[e:TO|FROM]->(object)  
        WHERE relation.rid = $rid  
        RETURN type(e) AS type, object.rid AS object
        """
    
    obj = read_object(tx, rid)

    member_records = tx.run(READ_DIRECTED_RELATION, rid=rid.string)
    from_members = []
    to_members = []

    for record in member_records:
        rid = record.get("object")
        direction = record.get("type")

        if direction == "FROM":
            from_members.append(rid)
        elif direction == "TO":
            to_members.append(rid)

    return {
        **obj._properties,
        "from": from_members,
        "to": to_members
    }
    
@execute_write
def delete(tx, rid: RID):
    delete_object(rid)
