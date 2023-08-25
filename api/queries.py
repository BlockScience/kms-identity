# Definitions

from rid_lib.means import (
    UndirectedRelation,
    DirectedRelation,
    UndirectedAssertion,
    DirectedAssertion
)

class TYPE:
    UNDIRECTED_MEMBER = "HAS"
    DIRECTED_FROM_MEMBER = "FROM"
    DIRECTED_TO_MEMBER = "TO"
    DEFINITION = "DEFINED_BY"

class TX:
    CREATE_UNDIRECTED = "create_undirected"
    CREATE_DIRECTED = "create_directed"
    FORK = "fork"
    UPDATE = "update"
    UPDATE_DEFINITION = "update_definition"
    UPDATE_UNDIRECTED_MEMBERS = "update_undirected_members"
    UPDATE_DIRECTED_MEMBERS = "update_directed_members"
    DELETE = "delete"

# Object Operations

CREATE_OBJECT = """
    MERGE (object {rid: $rid})
    SET object += $params
    RETURN object
"""

SET_LABEL = """
    MATCH (node)
    WHERE node.rid = $rid
    SET node:{}
"""

READ_OBJECT = """
    MATCH (o {rid: $rid})-[:REFERS_TO]->(d)  
    RETURN {rid: o.rid, data: properties(d)} AS result
"""

REFRESH_OBJECT = """
    MERGE (o {rid: $rid})  
    MERGE (o)-[:REFERS_TO]->(d:Data)  
    SET d = $params
"""

# Relation Operations

CREATE_UNDIRECTED = """
    CREATE (relation:{} {{rid: $rid}}) SET relation += $params  
    WITH relation  
    UNWIND $member_rids AS member_rid  
    MATCH (member) WHERE member.rid = member_rid  
    CREATE (relation)-[:HAS]->(member)  
    RETURN COLLECT(member.rid) AS members
"""

CREATE_DIRECTED = """
    CREATE (relation:{} {{rid: $rid}}) SET relation += $params
"""
      
CREATE_UNDIRECTED_RELATION = CREATE_UNDIRECTED.format(UndirectedRelation.label)
CREATE_DIRECTED_RELATION = CREATE_DIRECTED.format(DirectedRelation.label)

SET_DEFINITION = """
    MATCH (relation) WHERE relation.rid = $rid
    MATCH (definition) WHERE definition.rid = $definition_rid
    MERGE (relation)-[:DEFINED_BY]->(definition)
    RETURN definition.rid AS definition
"""

CREATE_FROM_EDGES = """
    MATCH (relation) WHERE relation.rid = $rid  
    UNWIND $from_rids AS from_rid  
    MATCH (from_node) WHERE from_node.rid = from_rid  
    CREATE (relation)-[:FROM]->(from_node)  
    RETURN COLLECT(from_node.rid) AS from
"""

CREATE_TO_EDGES = """
    MATCH (relation) WHERE relation.rid = $rid  
    UNWIND $to_rids AS to_rid  
    MATCH (to_node) WHERE to_node.rid = to_rid  
    CREATE (relation)-[:TO]->(to_node)  
    RETURN COLLECT(to_node.rid) AS to
"""

READ_RELATION = """
    MATCH (relation)  
    WHERE relation.rid = $rid  
    RETURN relation
"""

READ_UNDIRECTED_RELATION = """
    MATCH (relation)-[:HAS]->(object)  
    WHERE relation.rid = $rid  
    RETURN object.rid AS object
"""

READ_DIRECTED_RELATION = """
    MATCH (relation)-[e:TO|FROM]->(object)  
    WHERE relation.rid = $rid  
    RETURN type(e) AS type, object.rid AS object
"""

DELETE_RELATION = """
    MATCH (relation)  
    WHERE relation.rid = $rid  
    DETACH DELETE relation
"""

# Assertion Operations

CREATE_UNDIRECTED_ASSERTION = CREATE_UNDIRECTED.format(UndirectedAssertion.label)
CREATE_DIRECTED_ASSERTION = CREATE_DIRECTED.format(DirectedAssertion.label)

UPDATE_ASSERTION = """
    MATCH (assertion)  
    WHERE assertion.rid = $rid  
    SET assertion += $params
"""

REMOVE_DEFINITION = """
    MATCH (assertion)-[edge:DEFINED_BY]->(definition)
    WHERE assertion.rid = $rid
    DELETE edge
"""

ADD_MEMBERS_TO_ASSERTION = """
    MATCH (assertion:{})  
    WHERE assertion.rid = $rid  
    UNWIND $member_rids AS member_rid  
    MATCH (member) WHERE member.rid = member_rid  
    CREATE (assertion)-[:{}]->(member)  
    RETURN COLLECT(member.rid) AS members
"""

REMOVE_MEMBERS_FROM_ASSERTION = """
    MATCH (assertion:{})  
    WHERE assertion.rid = $rid  
    UNWIND $member_rids AS member_rid  
    MATCH (assertion)-[edge:{}]->(member) WHERE member.rid = member_rid  
    DELETE edge  
    RETURN COLLECT(member.rid) AS members
"""

ADD_MEMBERS_TO_UNDIRECTED_ASSERTION = ADD_MEMBERS_TO_ASSERTION.format(
    UndirectedAssertion.label, TYPE.UNDIRECTED_MEMBER)

REMOVE_MEMBERS_FROM_UNDIRECTED_ASSERTION = REMOVE_MEMBERS_FROM_ASSERTION.format(
    UndirectedAssertion.label, TYPE.UNDIRECTED_MEMBER
)

ADD_FROM_MEMBERS_TO_DIRECTED_ASSERTION = ADD_MEMBERS_TO_ASSERTION.format(
    DirectedAssertion.label, TYPE.DIRECTED_FROM_MEMBER
)

ADD_TO_MEMBERS_TO_DIRECTED_ASSERTION = ADD_MEMBERS_TO_ASSERTION.format(
    DirectedAssertion.label, TYPE.DIRECTED_TO_MEMBER
)

REMOVE_FROM_MEMBERS_FROM_DIRECTED_ASSERTION = REMOVE_MEMBERS_FROM_ASSERTION.format(
    DirectedAssertion.label, TYPE.DIRECTED_FROM_MEMBER
)

REMOVE_TO_MEMBERS_FROM_DIRECTED_ASSERTION = REMOVE_MEMBERS_FROM_ASSERTION.format(
    DirectedAssertion.label, TYPE.DIRECTED_TO_MEMBER
)

DELETE_ASSERTION = """
    MATCH (assertion)
    WHERE assertion.rid = $rid
    DETACH DELETE assertion
"""

INIT_TRANSACTION = """
    MATCH (assertion)  
    WHERE assertion.rid = $rid  
    CREATE (tx:Transaction $params)<-[:IS]-(assertion)  
    RETURN tx
"""

FORK_TRANSACTION = """
    MATCH (forked {rid: $forked_rid})-[:IS]->(prev:Transaction)
    MATCH (assertion {rid: $new_rid})
    CREATE (prev)<-[:PREV]-(tx:Transaction $params)<-[:IS]-(assertion)
    RETURN tx
"""

ADD_TRANSACTION = """
    MATCH (assertion)-[edge:IS]->(tx:Transaction)  
    WHERE assertion.rid = $rid  
    DELETE edge  
    CREATE (tx)<-[:PREV]-(ntx:Transaction $params)<-[:IS]-(assertion)  
    RETURN ntx AS tx
"""

READ_TRANSACTIONS = """
    MATCH (assertion)-[:IS|PREV*]->(tx:Transaction)
    WHERE assertion.rid = $rid
    RETURN tx
"""

# actions = [
#     "create",
#     "fork",
#     "update",
#     "delete",
#     "add_member",
#     "add_from",
#     "add_to",
#     "remove_member",
#     "remove_from",
#     "remove_to"
# ]