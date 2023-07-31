# Definitions

OBJECT_SYMBOL = "Object"
RELATION_SYMBOL = "Relation"
ASSERTION_SYMBOL = "Assertion"

DIRECTED_SYMBOL = "Directed"
UNDIRECTED_SYMBOL = "Undirected"

# Object Operations

CREATE_OBJECT = \
    "MERGE (object:Object {rid: $rid}) RETURN object"

READ_OBJECT = \
    "MATCH (o:Object {rid: $rid})-[:REFERS_TO]->(d) " \
    "RETURN {rid: o.rid, data: properties(d)} AS result"

REFRESH_OBJECT = \
    "MERGE (o:Object {rid: $rid}) " \
    "MERGE (o)-[:REFERS_TO]->(d:Data) " \
    "SET d = $props"

# Relation Operations

CREATE_UNDIRECTED = \
    "CREATE (relation:Undirected:{}) SET relation = $props " \
    "WITH relation " \
    "UNWIND $member_rids AS member_rid " \
    "MATCH (member) WHERE member.rid = member_rid " \
    "CREATE (relation)-[:HAS]->(member) " \
    "RETURN COLLECT(member.rid) AS members"

CREATE_DIRECTED = \
    "CREATE (relation:Directed:{}) SET relation = $props"
        
CREATE_UNDIRECTED_RELATION = CREATE_UNDIRECTED.format(RELATION_SYMBOL)
CREATE_DIRECTED_RELATION = CREATE_DIRECTED.format(RELATION_SYMBOL)

CREATE_FROM_EDGES = \
    "MATCH (relation:Directed) WHERE relation.rid = $rid " \
    "UNWIND $from_rids AS from_rid " \
    "MATCH (from_node) WHERE from_node.rid = from_rid " \
    "CREATE (relation)-[:FROM]->(from_node) " \
    "RETURN COLLECT(from_node.rid) AS from"
    
CREATE_TO_EDGES = \
    "MATCH (relation:Directed) WHERE relation.rid = $rid " \
    "UNWIND $to_rids AS to_rid " \
    "MATCH (to_node) WHERE to_node.rid = to_rid " \
    "CREATE (relation)-[:TO]->(to_node) " \
    "RETURN COLLECT(to_node.rid) AS to"

READ_RELATION = \
    "MATCH (relation:Relation|Assertion) " \
    "WHERE relation.rid = $rid " \
    "RETURN relation"

READ_UNDIRECTED_RELATION = \
    "MATCH (relation:Undirected)-[:HAS]->(object) " \
    "WHERE relation.rid = $rid " \
    "RETURN object.rid AS object"

READ_DIRECTED_RELATION = \
    "MATCH (relation:Directed)-[e:TO|FROM]->(object) " \
    "WHERE relation.rid = $rid " \
    "RETURN type(e) AS type, object.rid AS object"

DELETE_RELATION = \
    "MATCH (relation:Relation) " \
    "WHERE relation.rid = $rid " \
    "DETACH DELETE relation"

# Assertion Operations

CREATE_UNDIRECTED_ASSERTION = CREATE_UNDIRECTED.format(ASSERTION_SYMBOL)
CREATE_DIRECTED_ASSERTION = CREATE_DIRECTED.format(ASSERTION_SYMBOL)