# Definitions

OBJECT_LABEL = "Object"
RELATION_LABEL = "Relation"
ASSERTION_LABEL = "Assertion"
DIRECTED_LABEL = "Directed"
UNDIRECTED_LABEL = "Undirected"

UNDIRECTED_MEMBER_TYPE = "HAS"
DIRECTED_MEMBER_FROM_TYPE = "FROM"
DIRECTED_MEMBER_TO_TYPE = "TO"

# Object Operations

CREATE_OBJECT = """
    MERGE (object:Object {rid: $rid}) RETURN object
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
      
CREATE_UNDIRECTED_RELATION = CREATE_UNDIRECTED.format(RELATION_LABEL)
CREATE_DIRECTED_RELATION = CREATE_DIRECTED.format(RELATION_LABEL)

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

CREATE_UNDIRECTED_ASSERTION = CREATE_UNDIRECTED.format(ASSERTION_LABEL)
CREATE_DIRECTED_ASSERTION = CREATE_DIRECTED.format(ASSERTION_LABEL)

UPDATE_ASSERTION = """
    MATCH (assertion:Assertion)  
    WHERE assertion.rid = $rid  
    SET assertion += $props
"""

ADD_MEMBERS_TO_UNDIRECTED_ASSERTION = """
    MATCH (assertion:Assertion)  
    WHERE assertion.rid = $rid  
    UNWIND $member_rids AS member_rid  
    MATCH (member) WHERE member.rid = member_rid  
    CREATE (assertion)-[:HAS]->(member)  
    RETURN COLLECT(member.rid) AS members
"""

REMOVE_MEMBERS_FROM_UNDIRECTED_ASSERTION = """
    MATCH (assertion:Assertion)  
    WHERE assertion.rid = $rid  
    UNWIND $member_rids AS member_rid  
    MATCH (assertion)-[edge:HAS]->(member) WHERE member.rid = member_rid  
    DELETE edge  
    RETURN COLLECT(member.rid) AS members
"""

INIT_TRANSACTION = """
    MATCH (assertion:Assertion)  
    WHERE assertion.rid = $rid  
    CREATE (tx:Transaction $props)<-[:IS]-(assertion)  
    RETURN tx
"""

ADD_TRANSACTION = """
    MATCH (assertion:Assertion)-[edge:IS]->(tx:Transaction)  
    WHERE assertion.rid = $rid  
    DELETE edge  
    CREATE (tx)<-[:PREV]-(ntx:Transaction $props)<-[:IS]-(assertion)  
    RETURN ntx AS tx
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