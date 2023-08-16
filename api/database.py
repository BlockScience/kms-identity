import json
from api.utils import execute_read, execute_write
import rid_lib
from rid_lib import RID
from api.queries import *

@execute_write
def drop(tx):
    DROP = \
        "MATCH (n) DETACH DELETE n"
    tx.run(DROP)

# Object Operations

@execute_write
def create_object(tx, rid):
    rid = RID.from_string(rid)
    records = tx.run(CREATE_OBJECT, rid=rid.string, props=rid.dict)
    result = records.single()
    return result.get("object", None)

@execute_write
def refresh_object(tx, rid, data):
    tx.run(REFRESH_OBJECT, rid=rid, props=data)

@execute_read
def read_object(tx, rid):
    records = tx.run(READ_OBJECT, rid=rid)
    result = records.single()
    return result.get("result", None)

# Relation Operations

@execute_write
def create_undirected_relation(tx, obj):
    relation_rid = obj.get("rid")
    # removes self edges
    member_rids = [m for m in obj.pop("members") if m != relation_rid]

    records = tx.run(CREATE_UNDIRECTED_RELATION, props=obj, member_rids=member_rids)
    result = records.single()

    definition_rid = obj.get("definition", None)
    if definition_rid and (definition_rid != relation_rid):
        tx.run(SET_DEFINITION, rid=relation_rid, definition_rid=definition_rid)
    
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

    definition_rid = obj.get("definition", None)
    if definition_rid and (definition_rid != relation_rid):
        tx.run(SET_DEFINITION, rid=relation_rid, definition_rid=definition_rid)
    
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
    json_data = json.dumps(obj)
    rid = obj.get("rid")
    member_rids = obj.pop("members")

    records = tx.run(CREATE_UNDIRECTED_ASSERTION, props=obj, member_rids=member_rids)
    result = records.single()

    members = result.get("members")

    tx.run(INIT_TRANSACTION, rid=rid, props={
        "action": TX.CREATE_UNDIRECTED,
        "data": json_data
    })

    definition_rid = obj.get("definition", None)
    if definition_rid and (definition_rid != rid):
        tx.run(SET_DEFINITION, rid=rid, definition_rid=definition_rid)

    return {
        "rid": rid,
        "members": members
    }

@execute_write
def create_directed_assertion(tx, obj):
    json_data = json.dumps(obj)
    rid = obj.get("rid")
    from_rids = obj.pop("from")
    to_rids = obj.pop("to")

    tx.run(CREATE_DIRECTED_ASSERTION, props=obj)
    from_records = tx.run(CREATE_FROM_EDGES, rid=rid, from_rids=from_rids)
    to_records = tx.run(CREATE_TO_EDGES, rid=rid, to_rids=to_rids)

    from_result = from_records.single()
    to_result = to_records.single()

    definition_rid = obj.get("definition", None)
    if definition_rid and (definition_rid != rid):
        tx.run(SET_DEFINITION, rid=rid, definition_rid=definition_rid)

    tx.run(INIT_TRANSACTION, rid=rid, props={
        "action": TX.CREATE_DIRECTED,
        "data": json_data
    })

    return {
        "rid": rid,
        "from": from_result.get("from"),
        "to": to_result.get("to")
    }

@execute_write
def fork_assertion(db_tx, forked_rid, rid):
    tx_records = db_tx.run(READ_TRANSACTIONS, rid=forked_rid)

    history = []

    for record in tx_records:
        tx = record["tx"]._properties

        action = tx["action"]
        data = tx.get("data", None)

        history.append({
            "action": action,
            "data": json.loads(data) if data else None
        })

    history.reverse()

    for tx in history:
        action = tx["action"]
        data = tx.get("data", None)

        # overwrite rid from forked assertion
        if "rid" in data:
            data["rid"] = rid

        match action:
            case TX.CREATE_UNDIRECTED:
                member_rids = data.pop("members")
                db_tx.run(CREATE_UNDIRECTED_ASSERTION, props=data, member_rids=member_rids)

            case TX.CREATE_DIRECTED:
                from_rids = data.pop("from")
                to_rids = data.pop("to")
                db_tx.run(CREATE_DIRECTED_ASSERTION, props=data)
                db_tx.run(CREATE_FROM_EDGES, rid=rid, from_rids=from_rids)
                db_tx.run(CREATE_TO_EDGES, rid=rid, to_rids=to_rids)

            case TX.UPDATE:
                db_tx.run(UPDATE_ASSERTION, rid=rid, props=data)

            case TX.UPDATE_UNDIRECTED_MEMBERS:
                members_to_add = data.get("add", None)
                members_to_remove = data.get("remove", None)

                if members_to_add:
                    db_tx.run(ADD_MEMBERS_TO_UNDIRECTED_ASSERTION, rid=rid, member_rids=members_to_add)
                
                if members_to_remove:
                    db_tx.run(REMOVE_MEMBERS_FROM_UNDIRECTED_ASSERTION, rid=rid, member_rids=members_to_remove)
            
            case TX.UPDATE_DIRECTED_MEMBERS:
                members_to_add = data.get("add", None)
                members_to_remove = data.get("remove", None)

                if members_to_add:
                    from_members_to_add = members_to_add.get("from", None)
                    to_members_to_add = members_to_add.get("to", None)

                    if from_members_to_add:
                        db_tx.run(ADD_FROM_MEMBERS_TO_DIRECTED_ASSERTION, rid=rid, member_rids=from_members_to_add)
                    
                    if to_members_to_add:
                        db_tx.run(ADD_TO_MEMBERS_TO_DIRECTED_ASSERTION, rid=rid, member_rids=to_members_to_add)

                if members_to_remove:
                    from_members_to_remove = members_to_remove.get("from", None)
                    to_members_to_remove = members_to_remove.get("to", None)

                    if from_members_to_remove:
                        db_tx.run(REMOVE_FROM_MEMBERS_FROM_DIRECTED_ASSERTION, rid=rid, member_rids=from_members_to_remove)
                    
                    if to_members_to_remove:
                        db_tx.run(REMOVE_TO_MEMBERS_FROM_DIRECTED_ASSERTION, rid=rid, member_rids=to_members_to_remove)


    db_tx.run(FORK_TRANSACTION, forked_rid=forked_rid, new_rid=rid, props={
        "action": TX.FORK,
        "data": json.dumps({
            "rid": rid
        })
    })

@execute_write
def update_assertion(tx, rid, obj):
    tx.run(UPDATE_ASSERTION, rid=rid, props=obj)
    tx.run(ADD_TRANSACTION, rid=rid, props={
        "action": TX.UPDATE,
        "data": json.dumps(obj)
    })

@execute_write
def update_assertion_definition(tx, rid, obj):
    definition = obj.get("definition")

    if definition:
        tx.run(SET_DEFINITION, rid=rid, definition_rid=definition)
    else:
        tx.run(REMOVE_DEFINITION, rid=rid)

    tx.run(ADD_TRANSACTION, rid=rid, props={
        "action": TX.UPDATE_DEFINITION,
        "data": json.dumps(obj)
    })

@execute_write
def update_undirected_assertion_members(tx, rid, obj):
    members_to_add = obj.get("add", None)
    members_to_remove = obj.get("remove", None)

    if (not members_to_add) and (not members_to_remove):
        return

    if members_to_add:
        tx.run(ADD_MEMBERS_TO_UNDIRECTED_ASSERTION, rid=rid, member_rids=members_to_add)
    
    if members_to_remove:
        tx.run(REMOVE_MEMBERS_FROM_UNDIRECTED_ASSERTION, rid=rid, member_rids=members_to_remove)

    tx.run(ADD_TRANSACTION, rid=rid, props={
        "action": TX.UPDATE_UNDIRECTED_MEMBERS,
        "data": json.dumps(obj)
    })

@execute_write
def update_directed_assertion_members(tx, rid, obj):
    members_to_add = obj.get("add", None)
    members_to_remove = obj.get("remove", None)

    if (not members_to_add) and (not members_to_remove):
        return
    
    if members_to_add:
        from_members_to_add = members_to_add.get("from", None)
        to_members_to_add = members_to_add.get("to", None)

        if from_members_to_add:
            tx.run(ADD_FROM_MEMBERS_TO_DIRECTED_ASSERTION, rid=rid, member_rids=from_members_to_add)
        
        if to_members_to_add:
            tx.run(ADD_TO_MEMBERS_TO_DIRECTED_ASSERTION, rid=rid, member_rids=to_members_to_add)

    if members_to_remove:
        from_members_to_remove = members_to_remove.get("from", None)
        to_members_to_remove = members_to_remove.get("to", None)

        if from_members_to_remove:
            tx.run(REMOVE_FROM_MEMBERS_FROM_DIRECTED_ASSERTION, rid=rid, member_rids=from_members_to_remove)
        
        if to_members_to_remove:
            tx.run(REMOVE_TO_MEMBERS_FROM_DIRECTED_ASSERTION, rid=rid, member_rids=to_members_to_remove)

    tx.run(ADD_TRANSACTION, rid=rid, props={
        "action": TX.UPDATE_DIRECTED_MEMBERS,
        "data": json.dumps(obj)
    })

@execute_write
def delete_assertion(tx, rid):
    tx.run(ADD_TRANSACTION, rid=rid, props={
        "action": TX.DELETE
    })
    tx.run(DELETE_ASSERTION, rid=rid)