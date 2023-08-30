from .utils import *
from rid_lib import RID
from rid_lib.means import UndirectedAssertion, DirectedAssertion
import json

# Assertion Operations

@execute_write
def create_undirected(tx, rid: RID, params):
    json_data = json.dumps(params)
    member_rids = params.pop("members", [])
    definition_rid = params.get("definition", None)

    create_object(tx, rid, params)
    create_edges(tx, rid, "HAS", member_rids)

    if definition_rid and (definition_rid != rid.string):
        set_definition(tx, rid, definition_rid)

    init_transaction(tx, rid, "create", json_data)


@execute_write
def create_directed(tx, rid: RID, params):
    json_data = json.dumps(params)
    from_rids = params.pop("from", [])
    to_rids = params.pop("to", [])
    definition_rid = params.get("definition", None)

    create_object(tx, rid, params)
    create_edges(tx, rid, "FROM", from_rids)
    create_edges(tx, rid, "TO", to_rids)

    if definition_rid and (definition_rid != rid.string):
        set_definition(tx, rid, definition_rid)

    init_transaction(tx, rid, "create", json_data)


@execute_write
def get_transactions(tx, rid: RID):
    return read_transactions(tx, rid)

@execute_write
def fork(tx, forked_rid: RID, rid: RID):
    history = read_transactions(tx, forked_rid)

    print(history)

    for transaction in history:
        means = transaction["means"]
        action = transaction["action"]
        params = transaction.get("context", None)

        match (means, action):
            case (UndirectedAssertion.symbol, "create"):
                member_rids = params.pop("members", [])
                definition_rid = params.pop("definition", None)
                
                create_object(tx, rid, params)
                create_edges(tx, rid, "HAS", member_rids)

                if definition_rid and (definition_rid != rid.string):
                    set_definition(tx, rid, definition_rid)

            case (DirectedAssertion.symbol, "create"):
                from_rids = params.pop("from", [])
                to_rids = params.pop("to", [])
                definition_rid = params.get("definition", None)

                create_object(tx, rid, params)
                create_edges(tx, rid, "FROM", from_rids)
                create_edges(tx, rid, "TO", to_rids)

                if definition_rid and (definition_rid != rid.string):
                    set_definition(tx, rid, definition_rid)

            case (_, "update"):
                update_object(tx, rid, params)

            case (_, "update_definition"):
                definition = params.get("definition", None)
                if definition:
                    set_definition(tx, rid, definition)
                else:
                    unset_definition(tx, rid)

            case (UndirectedAssertion.symbol, "update_members"):
                members_to_add = params.get("add", None)
                members_to_remove = params.get("remove", None)

                if members_to_add:
                    add_edges(tx, rid, "HAS", members_to_add)
                
                if members_to_remove:
                    remove_edges(tx, rid, "HAS", members_to_remove)
            
            case (DirectedAssertion.symbol, "update_members"):
                members_to_add = params.get("add", None)
                members_to_remove = params.get("remove", None)
                
                if members_to_add:
                    from_members_to_add = members_to_add.get("from", None)
                    to_members_to_add = members_to_add.get("to", None)

                    if from_members_to_add:
                        add_edges(tx, rid, "FROM", from_members_to_add)
                    
                    if to_members_to_add:
                        add_edges(tx, rid, "TO", to_members_to_add)

                if members_to_remove:
                    from_members_to_remove = members_to_remove.get("from", None)
                    to_members_to_remove = members_to_remove.get("to", None)

                    if from_members_to_remove:
                        remove_edges(tx, rid, "FROM", from_members_to_remove)
                    
                    if to_members_to_remove:
                        remove_edges(tx, rid, "TO", to_members_to_remove)

    fork_transaction(tx, forked_rid, rid, "fork")

    return rid

@execute_write
def update(tx, rid: RID, params):
    update_object(tx, rid, params)
    add_transaction(tx, rid, "update", json.dumps(params))


@execute_write
def update_definition(tx, rid: RID, params):
    definition = params.get("definition", None)

    if definition:
        set_definition(tx, rid, definition)
    else:
        unset_definition(tx, rid)

    add_transaction(tx, rid, "update_definition", json.dumps(params))


@execute_write
def update_undirected_members(tx, rid: RID, params):
    members_to_add = params.get("add", None)
    members_to_remove = params.get("remove", None)

    if (not members_to_add) and (not members_to_remove):
        return

    if members_to_add:
        add_edges(tx, rid, "HAS", members_to_add)
    
    if members_to_remove:
        remove_edges(tx, rid, "HAS", members_to_remove)

    add_transaction(tx, rid, "update_members", json.dumps(params))


@execute_write
def update_directed_members(tx, rid: RID, params):
    members_to_add = params.get("add", None)
    members_to_remove = params.get("remove", None)

    if (not members_to_add) and (not members_to_remove):
        return
    
    if members_to_add:
        from_members_to_add = members_to_add.get("from", None)
        to_members_to_add = members_to_add.get("to", None)

        if from_members_to_add:
            add_edges(tx, rid, "FROM", from_members_to_add)
        
        if to_members_to_add:
            add_edges(tx, rid, "TO", to_members_to_add)

    if members_to_remove:
        from_members_to_remove = members_to_remove.get("from", None)
        to_members_to_remove = members_to_remove.get("to", None)

        if from_members_to_remove:
            remove_edges(tx, rid, "FROM", from_members_to_remove)
        
        if to_members_to_remove:
            remove_edges(tx, rid, "TO", to_members_to_remove)
    
    add_transaction(tx, rid, "update_members", json.dumps(params))


@execute_write
def delete(tx, rid: RID):
    add_transaction(tx, rid, "delete")
    delete_object(tx, rid)
