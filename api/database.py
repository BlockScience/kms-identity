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
def create_object(tx, rid: RID):
    records = tx.run(CREATE_OBJECT, rid=rid.string, params={
        "means": rid.means.symbol,
        "reference": rid.reference
    })
    result = records.single()
    return result.get("object", None)

@execute_write
def refresh_object(tx, rid: RID, params):
    tx.run(REFRESH_OBJECT, rid=rid.string, params=params)

@execute_read
def read_object(tx, rid: RID):
    records = tx.run(READ_OBJECT, rid=rid.string)
    result = records.single()
    if result:
        return result.get("result", None)

# Relation Operations

@execute_write
def create_undirected_relation(tx, rid: RID, params):
    # removes self edges
    member_rids = [m for m in params.pop("members", []) if m != rid.string]

    records = tx.run(CREATE_UNDIRECTED_RELATION, rid=rid.string, params=params, member_rids=member_rids)
    result = records.single()

    definition_rid = params.get("definition", None)
    if definition_rid and (definition_rid != rid.string):
        tx.run(SET_DEFINITION, rid=rid.string, definition_rid=definition_rid)
    
    return rid, {
        "rid": rid.string,
        "members": result.get("members")
    }

@execute_write
def create_directed_relation(tx, rid: RID, params):
    # removes self edges
    from_rids = [m for m in params.pop("from", []) if m != rid.string]
    to_rids = [m for m in params.pop("to", []) if m != rid.string]
    
    tx.run(CREATE_DIRECTED_RELATION, rid=rid.string, params=params)
    from_records = tx.run(CREATE_FROM_EDGES, rid=rid.string, from_rids=from_rids)
    to_records = tx.run(CREATE_TO_EDGES, rid=rid.string, to_rids=to_rids)

    from_result = from_records.single()
    to_result = to_records.single()

    definition_rid = params.get("definition", None)
    if definition_rid and (definition_rid != rid.string):
        tx.run(SET_DEFINITION, rid=rid.string, definition_rid=definition_rid)
    
    return rid, {
        "rid": rid.string,
        "from": from_result.get("from"),
        "to": to_result.get("to")
    }
    
@execute_read
def read_relation(tx, rid: RID):
    records = tx.run(READ_RELATION, rid=rid.string)
    result = records.single()

    if not result:
        return None
    
    relation = result.get("relation")

    if "Undirected" in relation.labels:
        member_records = tx.run(READ_UNDIRECTED_RELATION, rid=rid.string)
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
        member_records = tx.run(READ_DIRECTED_RELATION, rid=rid.string)
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
def delete_relation(tx, rid: RID):
    tx.run(DELETE_RELATION, rid=rid.string)

# Assertion Operations

@execute_write
def create_undirected_assertion(tx, rid: RID, params):
    json_data = json.dumps(params)
    member_rids = params.pop("members", [])
    label = params.pop("label", None)

    records = tx.run(CREATE_UNDIRECTED_ASSERTION, rid=rid.string, params=params, member_rids=member_rids)
    result = records.single()

    if label:
        tx.run(SET_LABEL.format(label), rid=rid.string)

    members = result.get("members")

    tx.run(INIT_TRANSACTION, rid=rid.string, params={
        "action": TX.CREATE_UNDIRECTED,
        "data": json_data
    })

    definition_rid = params.get("definition", None)
    if definition_rid and (definition_rid != rid.string):
        tx.run(SET_DEFINITION, rid=rid.string, definition_rid=definition_rid)

    return rid, {
        "rid": rid.string,
        "members": members
    }

@execute_write
def create_directed_assertion(tx, rid: RID, params):
    json_data = json.dumps(params)
    from_rids = params.pop("from", [])
    to_rids = params.pop("to", [])
    label = params.pop("label", None)

    tx.run(CREATE_DIRECTED_ASSERTION, rid=rid.string, params=params)
    from_records = tx.run(CREATE_FROM_EDGES, rid=rid.string, from_rids=from_rids)
    to_records = tx.run(CREATE_TO_EDGES, rid=rid.string, to_rids=to_rids)

    if label:
        tx.run(SET_LABEL.format(label), rid=rid.string)

    from_result = from_records.single()
    to_result = to_records.single()

    definition_rid = params.get("definition", None)
    if definition_rid and (definition_rid != rid.string):
        tx.run(SET_DEFINITION, rid=rid.string, definition_rid=definition_rid)

    tx.run(INIT_TRANSACTION, rid=rid.string, params={
        "action": TX.CREATE_DIRECTED,
        "data": json_data
    })

    return rid, {
        "rid": rid.string,
        "from": from_result.get("from"),
        "to": to_result.get("to")
    }

@execute_write
def fork_assertion(tx, rid: RID, new_rid: RID):
    tx_records = tx.run(READ_TRANSACTIONS, rid=rid.string)

    history = []

    for record in tx_records:
        transaction = record["tx"]._properties

        action = transaction["action"]
        data = transaction.get("data", None)

        history.append({
            "action": action,
            "data": json.loads(data) if data else None
        })

    history.reverse()

    for transaction in history:
        action = transaction["action"]
        data = transaction.get("data", None)

        # overwrite rid from forked assertion
        if "rid" in data:
            data["rid"] = rid

        match action:
            case TX.CREATE_UNDIRECTED:
                member_rids = data.pop("members", [])
                tx.run(CREATE_UNDIRECTED_ASSERTION, rid=new_rid.string, params=data, member_rids=member_rids)

            case TX.CREATE_DIRECTED:
                from_rids = data.pop("from", [])
                to_rids = data.pop("to", [])
                tx.run(CREATE_DIRECTED_ASSERTION, rid=new_rid.string, params=data)
                tx.run(CREATE_FROM_EDGES, rid=new_rid.string, from_rids=from_rids)
                tx.run(CREATE_TO_EDGES, rid=new_rid.string, to_rids=to_rids)

            case TX.UPDATE:
                tx.run(UPDATE_ASSERTION, rid=new_rid.string, params=data)

            case TX.UPDATE_UNDIRECTED_MEMBERS:
                members_to_add = data.get("add", None)
                members_to_remove = data.get("remove", None)

                if members_to_add:
                    tx.run(ADD_MEMBERS_TO_UNDIRECTED_ASSERTION, rid=new_rid.string, member_rids=members_to_add)
                
                if members_to_remove:
                    tx.run(REMOVE_MEMBERS_FROM_UNDIRECTED_ASSERTION, rid=new_rid.string, member_rids=members_to_remove)
            
            case TX.UPDATE_DIRECTED_MEMBERS:
                members_to_add = data.get("add", None)
                members_to_remove = data.get("remove", None)

                if members_to_add:
                    from_members_to_add = members_to_add.get("from", None)
                    to_members_to_add = members_to_add.get("to", None)

                    if from_members_to_add:
                        tx.run(ADD_FROM_MEMBERS_TO_DIRECTED_ASSERTION, rid=new_rid.string, member_rids=from_members_to_add)
                    
                    if to_members_to_add:
                        tx.run(ADD_TO_MEMBERS_TO_DIRECTED_ASSERTION, rid=new_rid.string, member_rids=to_members_to_add)

                if members_to_remove:
                    from_members_to_remove = members_to_remove.get("from", None)
                    to_members_to_remove = members_to_remove.get("to", None)

                    if from_members_to_remove:
                        tx.run(REMOVE_FROM_MEMBERS_FROM_DIRECTED_ASSERTION, rid=new_rid.string, member_rids=from_members_to_remove)
                    
                    if to_members_to_remove:
                        tx.run(REMOVE_TO_MEMBERS_FROM_DIRECTED_ASSERTION, rid=new_rid.string, member_rids=to_members_to_remove)


    tx.run(FORK_TRANSACTION, forked_rid=rid.string, new_rid=new_rid.string, params={
        "action": TX.FORK,
        "data": json.dumps({
            "rid": new_rid.string
        })
    })

    return new_rid

@execute_write
def update_assertion(tx, rid: RID, params):
    tx.run(UPDATE_ASSERTION, rid=rid.string, params=params)
    tx.run(ADD_TRANSACTION, rid=rid.string, params={
        "action": TX.UPDATE,
        "data": json.dumps(params)
    })

@execute_write
def update_assertion_definition(tx, rid: RID, params):
    definition = params.get("definition")

    if definition:
        tx.run(SET_DEFINITION, rid=rid.string, definition_rid=definition)
    else:
        tx.run(REMOVE_DEFINITION, rid=rid.string)

    tx.run(ADD_TRANSACTION, rid=rid.string, params={
        "action": TX.UPDATE_DEFINITION,
        "data": json.dumps(params)
    })

@execute_write
def update_undirected_assertion_members(tx, rid: RID, params):
    members_to_add = params.get("add", None)
    members_to_remove = params.get("remove", None)

    if (not members_to_add) and (not members_to_remove):
        return

    if members_to_add:
        tx.run(ADD_MEMBERS_TO_UNDIRECTED_ASSERTION, rid=rid.string, member_rids=members_to_add)
    
    if members_to_remove:
        tx.run(REMOVE_MEMBERS_FROM_UNDIRECTED_ASSERTION, rid=rid.string, member_rids=members_to_remove)

    tx.run(ADD_TRANSACTION, rid=rid.string, params={
        "action": TX.UPDATE_UNDIRECTED_MEMBERS,
        "data": json.dumps(params)
    })

@execute_write
def update_directed_assertion_members(tx, rid: RID, params):
    members_to_add = params.get("add", None)
    members_to_remove = params.get("remove", None)

    if (not members_to_add) and (not members_to_remove):
        return
    
    if members_to_add:
        from_members_to_add = members_to_add.get("from", None)
        to_members_to_add = members_to_add.get("to", None)

        if from_members_to_add:
            tx.run(ADD_FROM_MEMBERS_TO_DIRECTED_ASSERTION, rid=rid.string, member_rids=from_members_to_add)
        
        if to_members_to_add:
            tx.run(ADD_TO_MEMBERS_TO_DIRECTED_ASSERTION, rid=rid.string, member_rids=to_members_to_add)

    if members_to_remove:
        from_members_to_remove = members_to_remove.get("from", None)
        to_members_to_remove = members_to_remove.get("to", None)

        if from_members_to_remove:
            tx.run(REMOVE_FROM_MEMBERS_FROM_DIRECTED_ASSERTION, rid=rid.string, member_rids=from_members_to_remove)
        
        if to_members_to_remove:
            tx.run(REMOVE_TO_MEMBERS_FROM_DIRECTED_ASSERTION, rid=rid.string, member_rids=to_members_to_remove)

    tx.run(ADD_TRANSACTION, rid=rid.string, params={
        "action": TX.UPDATE_DIRECTED_MEMBERS,
        "data": json.dumps(params)
    })

@execute_write
def delete_assertion(tx, rid: RID):
    tx.run(ADD_TRANSACTION, rid=rid.string, params={
        "action": TX.DELETE
    })
    tx.run(DELETE_ASSERTION, rid=rid.string)