from api.core import driver
from api.config import NEO4J_DB
import functools, json

def execute_read(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with driver.session(database=NEO4J_DB) as session:
            return session.execute_read(func, *args, **kwargs)
    return wrapper

def execute_write(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with driver.session(database=NEO4J_DB) as session:
            return session.execute_write(func, *args, **kwargs)
    return wrapper

def set_labels(tx, rid, labels):
    SET_LABEL = """
        MATCH (node)
        WHERE node.rid = $rid
        SET node:{}
        """
    
    for label in labels:
        tx.run(SET_LABEL.format(label), rid=rid.string)

def create_object(tx, rid, params={}):
    CREATE_OBJECT = """
        MERGE (object {rid: $rid})
        SET object += $params
        RETURN object
        """
    
    tx.run(CREATE_OBJECT, rid=rid.string, params=params)
    set_labels(tx, rid, rid.labels)

def read_object(tx, rid):
    READ_OBJECT = """
        MATCH (object)  
        WHERE object.rid = $rid  
        RETURN object
    """

    records = tx.run(READ_OBJECT, rid=rid.string)
    result = records.single()
    return result.get("object") if result else None

def update_object(tx, rid, params):
    UPDATE_OBJECT = """
        MATCH (object)  
        WHERE object.rid = $rid  
        SET object += $params
        """
    
    tx.run(UPDATE_OBJECT, rid=rid.string, params=params)

def delete_object(tx, rid):
    DELETE_OBJECT = """
        MATCH (object)
        WHERE object.rid = $rid
        DETACH DELETE object
        """
    
    tx.run(DELETE_OBJECT, rid=rid.string)

def create_edges(tx, rid, type, members):
    CREATE_EDGES = """
        MATCH (relation) WHERE relation.rid = $rid  
        UNWIND $member_rids AS member_rid  
        MATCH (member) WHERE member.rid = member_rid  
        CREATE (relation)-[:{}]->(member)  
        RETURN COLLECT(member.rid) AS member
        """
    
    tx.run(CREATE_EDGES.format(type), rid=rid.string, member_rids=members)

def add_edges(tx, rid, type, members):
    ADD_EDGES = """
        MATCH (assertion)  
        WHERE assertion.rid = $rid  
        UNWIND $member_rids AS member_rid  
        MATCH (member) WHERE member.rid = member_rid  
        CREATE (assertion)-[:{}]->(member)  
        RETURN COLLECT(member.rid) AS members
        """
    
    tx.run(ADD_EDGES.format(type), rid=rid.string, member_rids=members)

def remove_edges(tx, rid, type, members):
    REMOVE_EDGES = """
        MATCH (assertion)  
        WHERE assertion.rid = $rid  
        UNWIND $member_rids AS member_rid  
        MATCH (assertion)-[edge:{}]->(member) WHERE member.rid = member_rid  
        DELETE edge  
        RETURN COLLECT(member.rid) AS members
        """
    
    tx.run(REMOVE_EDGES.format(type), rid=rid.string, member_rids=members)

def set_definition(tx, rid, definition):
    SET_DEFINITION = """
        MATCH (relation) WHERE relation.rid = $rid
        MATCH (definition) WHERE definition.rid = $definition_rid
        MERGE (relation)-[:DEFINED_BY]->(definition)
        RETURN definition.rid AS definition
        """
    
    tx.run(SET_DEFINITION, rid=rid.string, definition_rid=definition)

def unset_definition(tx, rid):
    UNSET_DEFINITION = """
        MATCH (assertion)-[edge:DEFINED_BY]->(definition)
        WHERE assertion.rid = $rid
        DELETE edge
        """
    
    tx.run(UNSET_DEFINITION, rid=rid.string)

def init_transaction(tx, rid, action, context="{}"):
    INIT_TRANSACTION = """
        MATCH (assertion)  
        WHERE assertion.rid = $rid  
        CREATE (tx:Transaction $params)<-[:IS]-(assertion)  
        RETURN tx
        """
    
    tx.run(INIT_TRANSACTION, rid=rid.string, params={
        "means": rid.means.symbol,
        "action": action,
        "context": context
    })

def fork_transaction(tx, forked_rid, new_rid, action, context="{}"):
    FORK_TRANSACTION = """
        MATCH (forked {rid: $forked_rid})-[:IS]->(prev:Transaction)
        MATCH (assertion {rid: $new_rid})
        CREATE (prev)<-[:PREV]-(tx:Transaction $params)<-[:IS]-(assertion)
        RETURN tx
        """

    tx.run(FORK_TRANSACTION, forked_rid=forked_rid.string, new_rid=new_rid.string, params={
        "means": forked_rid.means.symbol,
        "action": action,
        "context": context
    })

def add_transaction(tx, rid, action, context="{}"):
    ADD_TRANSACTION = """
        MATCH (assertion)-[edge:IS]->(tx:Transaction)  
        WHERE assertion.rid = $rid  
        DELETE edge  
        CREATE (tx)<-[:PREV]-(ntx:Transaction $params)<-[:IS]-(assertion)  
        RETURN ntx AS tx
        """
    
    tx.run(ADD_TRANSACTION, rid=rid.string, params={
        "means": rid.means.symbol,
        "action": action,
        "context": context
    })

def read_transactions(tx, rid):
    READ_TRANSACTIONS = """
        MATCH (assertion)-[:IS|PREV*]->(tx:Transaction)
        WHERE assertion.rid = $rid
        RETURN tx
        """
    
    tx_records = tx.run(READ_TRANSACTIONS, rid=rid.string)
    history = []

    for record in tx_records:
        transaction = record["tx"]._properties
        context_json = transaction.get("context", None)
        if context_json:
            transaction["context"] = json.loads(context_json)

        history.append(transaction)
    history.reverse()

    return history