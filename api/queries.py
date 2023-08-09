# Definitions

class LABEL:
    OBJECT = "Object"
    RELATION = "Relation"
    ASSERTION = "Assertion"
    DIRECTED = "Directed"
    UNDIRECTED = "Undirected"

class TYPE:
    UNDIRECTED_MEMBER = "HAS"
    DIRECTED_FROM_MEMBER = "FROM"
    DIRECTED_TO_MEMBER = "TO"

class TX:
    CREATE_UNDIRECTED = "create_undirected"
    CREATE_DIRECTED = "create_directed"
    FORK = "fork"
    UPDATE = "update"
    UPDATE_UNDIRECTED_MEMBERS = "update_undirected_members"
    UPDATE_DIRECTED_MEMBERS = "update_directed_members"
    DELETE = "delete"

# Object Operations

CREATE_OBJECT = """
    MERGE (object:Object {rid: $rid}) SET object += $props RETURN object
"""

READ_OBJECT = """
    MATCH (o:Object {rid: $rid})-[:REFERS_TO]->(d)  
    RETURN {rid: o.rid, data: properties(d)} AS result
"""

REFRESH_OBJECT = """
    MERGE (o:Object {rid: $rid})  
    MERGE (o)-[:REFERS_TO]->(d:Data)  
    SET d = $props
"""

# Relation Operations

CREATE_UNDIRECTED = """
    CREATE (relation:Undirected:{}) SET relation = $props  
    WITH relation  
    UNWIND $member_rids AS member_rid  
    MATCH (member) WHERE member.rid = member_rid  
    CREATE (relation)-[:HAS]->(member)  
    RETURN COLLECT(member.rid) AS members
"""

CREATE_DIRECTED = """
    CREATE (relation:Directed:{}) SET relation = $props
"""
      
CREATE_UNDIRECTED_RELATION = CREATE_UNDIRECTED.format(LABEL.RELATION)
CREATE_DIRECTED_RELATION = CREATE_DIRECTED.format(LABEL.RELATION)

CREATE_FROM_EDGES = """
    MATCH (relation:Directed) WHERE relation.rid = $rid  
    UNWIND $from_rids AS from_rid  
    MATCH (from_node) WHERE from_node.rid = from_rid  
    CREATE (relation)-[:FROM]->(from_node)  
    RETURN COLLECT(from_node.rid) AS from
"""

CREATE_TO_EDGES = """
    MATCH (relation:Directed) WHERE relation.rid = $rid  
    UNWIND $to_rids AS to_rid  
    MATCH (to_node) WHERE to_node.rid = to_rid  
    CREATE (relation)-[:TO]->(to_node)  
    RETURN COLLECT(to_node.rid) AS to
"""

READ_RELATION = """
    MATCH (relation:Relation|Assertion)  
    WHERE relation.rid = $rid  
    RETURN relation
"""

READ_UNDIRECTED_RELATION = """
    MATCH (relation:Undirected)-[:HAS]->(object)  
    WHERE relation.rid = $rid  
    RETURN object.rid AS object
"""

READ_DIRECTED_RELATION = """
    MATCH (relation:Directed)-[e:TO|FROM]->(object)  
    WHERE relation.rid = $rid  
    RETURN type(e) AS type, object.rid AS object
"""

DELETE_RELATION = """
    MATCH (relation:Relation)  
    WHERE relation.rid = $rid  
    DETACH DELETE relation
"""

# Assertion Operations

CREATE_UNDIRECTED_ASSERTION = CREATE_UNDIRECTED.format(LABEL.ASSERTION)
CREATE_DIRECTED_ASSERTION = CREATE_DIRECTED.format(LABEL.ASSERTION)

UPDATE_ASSERTION = """
    MATCH (assertion:Assertion)  
    WHERE assertion.rid = $rid  
    SET assertion += $props
"""

ADD_MEMBERS_TO_ASSERTION = """
    MATCH (assertion:{}:Assertion)  
    WHERE assertion.rid = $rid  
    UNWIND $member_rids AS member_rid  
    MATCH (member) WHERE member.rid = member_rid  
    CREATE (assertion)-[:{}]->(member)  
    RETURN COLLECT(member.rid) AS members
"""

REMOVE_MEMBERS_FROM_ASSERTION = """
    MATCH (assertion:{}:Assertion)  
    WHERE assertion.rid = $rid  
    UNWIND $member_rids AS member_rid  
    MATCH (assertion)-[edge:{}]->(member) WHERE member.rid = member_rid  
    DELETE edge  
    RETURN COLLECT(member.rid) AS members
"""

ADD_MEMBERS_TO_UNDIRECTED_ASSERTION = ADD_MEMBERS_TO_ASSERTION.format(
    LABEL.UNDIRECTED, TYPE.UNDIRECTED_MEMBER)

REMOVE_MEMBERS_FROM_UNDIRECTED_ASSERTION = REMOVE_MEMBERS_FROM_ASSERTION.format(
    LABEL.UNDIRECTED, TYPE.UNDIRECTED_MEMBER
)

ADD_FROM_MEMBERS_TO_DIRECTED_ASSERTION = ADD_MEMBERS_TO_ASSERTION.format(
    LABEL.DIRECTED, TYPE.DIRECTED_FROM_MEMBER
)

ADD_TO_MEMBERS_TO_DIRECTED_ASSERTION = ADD_MEMBERS_TO_ASSERTION.format(
    LABEL.DIRECTED, TYPE.DIRECTED_TO_MEMBER
)

REMOVE_FROM_MEMBERS_FROM_DIRECTED_ASSERTION = REMOVE_MEMBERS_FROM_ASSERTION.format(
    LABEL.DIRECTED, TYPE.DIRECTED_FROM_MEMBER
)

REMOVE_TO_MEMBERS_FROM_DIRECTED_ASSERTION = REMOVE_MEMBERS_FROM_ASSERTION.format(
    LABEL.DIRECTED, TYPE.DIRECTED_TO_MEMBER
)

DELETE_ASSERTION = """
    MATCH (assertion:Assertion)
    WHERE assertion.rid = $rid
    DETACH DELETE assertion
"""

INIT_TRANSACTION = """
    MATCH (assertion:Assertion)  
    WHERE assertion.rid = $rid  
    CREATE (tx:Transaction $props)<-[:IS]-(assertion)  
    RETURN tx
"""

FORK_TRANSACTION = """
    MATCH (forked:Assertion {rid: $forked_rid})-[:IS]->(prev:Transaction)
    MATCH (assertion:Assertion {rid: $new_rid})
    CREATE (prev)<-[:PREV]-(tx:Transaction $props)<-[:IS]-(assertion)
    RETURN tx
"""

ADD_TRANSACTION = """
    MATCH (assertion:Assertion)-[edge:IS]->(tx:Transaction)  
    WHERE assertion.rid = $rid  
    DELETE edge  
    CREATE (tx)<-[:PREV]-(ntx:Transaction $props)<-[:IS]-(assertion)  
    RETURN ntx AS tx
"""

READ_TRANSACTIONS = """
    MATCH (assertion:Assertion)-[:IS|PREV*]->(tx:Transaction)
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