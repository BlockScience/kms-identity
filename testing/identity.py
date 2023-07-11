from utils import execute, exit, READ, WRITE
import nanoid


@execute(WRITE)
def create_identity(tx, props):
    id_ = nanoid.generate()
    props['id'] = id_
    id2 = nanoid.generate()
    query = "CREATE (i:Identity $props)-[:IS]->(t:Transaction {id2: $id2}) RETURN i"
    result = tx.run(query, {'props': props, 'id2': id2})
    return id_

@execute(WRITE)
def update_identity(tx, id_, props):
    props.pop('id', None)
    query = "MATCH (i:Identity) WHERE i.id = $id_ SET i = $props"
    result = tx.run(query, id_=id_)

@execute(READ)
def read_identity(tx, id_):
    query = "MATCH (i:Identity) WHERE i.id = $id_ RETURN i"
    result = tx.run(query, id_=id_)
    return result.single().data()

@execute(WRITE)
def create_knowledge(tx, props):
    id_ = nanoid.generate()
    props['id'] = id_
    query = "CREATE (k:Knowledge $props) RETURN k"
    result = tx.run(query, {'props': props})
    return id_

@execute(WRITE)
def add_member(tx, iid, kid):
    query = """MATCH (i:Identity) WHERE i.id = $iid
    MATCH (k:Knowledge|Identity) WHERE k.id = $kid
    MERGE (i)-[:HAS]->(k)"""
    result = tx.run(query, iid=iid, kid=kid)

@execute(WRITE)
def add_transaction(tx, iid, props):
    id_ = nanoid.generate()
    props['id'] = id_
    query = """MATCH (i:Identity {id: $iid})-[r:IS]->(p:Transaction)
    DELETE r
    CREATE (p)-[:SUCCEEDS]->(n:Transaction $props)<-[:IS]-(i)"""
    result = tx.run(query, iid=iid, props=props)

@execute(WRITE)
def wipe(tx):
    query = "MATCH (n) DETACH DELETE n"
    tx.run(query)

wipe()

iobj = create_identity({'name': 'Luke', 'type': 'user'})
kobj = create_knowledge({'name': 'KOI Identity', 'type': 'HackMD'})
add_member(iobj, kobj)

input()

add_transaction(iobj, {})

exit()