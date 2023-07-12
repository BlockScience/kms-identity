CREATE_OBJECT_REFERENCE = \
    "CREATE (r:Reference) SET i = $props RETURN r AS result"

READ_OBJECT = \
    "MATCH (r:Reference)-[:REFERS_TO]->(d) RETURN {id: r.id, uri: r.uri, data: properties(d)} AS result"

REFRESH_OBJECT = \
    "MERGE (r:Reference {id: $id})-[:REFERS_TO]->(d:Data) " \
    "SET d = $props"

GET_OBJECT_DEREFERENCE = \
    "MATCH (r:Reference {id: $id})<-[:HAS]-(i:Identity {type: 'controller'}) RETURN [r.uri, i.dereference] AS result"

CREATE_IDENTITY = \
    "CREATE (i:Identity {id: $id}) SET i += $props " \
    "CREATE (i)-[:IS]->(t:Transaction {log: $log})"

READ_IDENTITY = \
    "MATCH (i:Identity {id: $id}) RETURN i AS result"

UPDATE_IDENTITY = \
    "MERGE (i:Identity {id: $id}) SET i += $props RETURN i AS result"

DELETE_IDENTITY = \
    "MREGE (i:Identity {id: $id}) DETACH DELETE i"

FORK_IDENTITY = \
    "MATCH (:Identity {id: $m_id})-[:IS]->(p:Transaction) " \
    "CREATE (i:Identity $props)-[:IS]->(n:Transaction {log: $log})-[:SUCCEEDS]->(p)"