CREATE_OBJECT_REFERENCE = \
    "CREATE (i:Reference) SET i = $props"

CREATE_IDENTITY = \
    "CREATE (i:Identity {id: $id}) SET i += $props " \
    "CREATE (i)-[:IS]->(t:Transaction {log: $log})"

READ_IDENTITY = \
    "MATCH (i:Identity {id: $id}) RETURN i"

UPDATE_IDENTITY = \
    "MERGE (i:Identity {id: $id}) SET i += $props RETURN i"

DELETE_IDENTITY = \
    "MREGE (i:Identity {id: $id}) DETACH DELETE i"

FORK_IDENTITY = \
    "MATCH (:Identity {id: $m_id})-[:IS]->(p:Transaction) " \
    "CREATE (i:Identity $props)-[:IS]->(n:Transaction {log: $log})-[:SUCCEEDS]->(p)"