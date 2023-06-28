import nanoid
import functools
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

driver = GraphDatabase.driver(URI, auth=AUTH)
print('Connected to DB')

READ = "read"
WRITE = "write"

def execute(mode, db="neo4j"):
    def execute_internal(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            with driver.session(database=db) as session:
                print('Opened session')
                if mode == READ:
                    result = session.execute_read(method, *args, **kwargs)
                elif mode == WRITE:
                    result = session.execute_write(method, *args, **kwargs)
                return result
        return wrapper
    return execute_internal

class Identity:
    def __init__(self, id) -> None:
        self.id = id
        self.data = None

    @execute(READ)
    def load(tx, self):
        query = "MATCH (i:Identity {id: $id}) RETURN i"
        result = tx.run(query, id=self.id)
        data = result.single()
        if data:
            self.data = data.data()
            return True
        else:
            return False

    @execute(WRITE)
    def save(tx, self):
        query = "MERGE (i:Identity {id: $id}) SET i += $props RETURN i"
        # this will cause a race condition
        self.add_transaction(f"UPDATE {self.id} {self.data}")
        result = tx.run(query, id=self.id, props=self.data)

    @execute(WRITE)
    def create(tx, self, props):
        print(tx, self, props)
        query = "CREATE (i:Identity {id: $id}) SET i += $props " \
        "CREATE (i)-[:IS]->(t:Transaction {log: $log})"
        log = f"CREATE {self.id} {props}"
        result = tx.run(query, id=self.id, props=props, log=log)

    @execute(WRITE)
    def add_child(tx, self, bid):
        query = "MATCH (a:Identity {id: $aid}) " \
        "MATCH (b:Identity|Knowledge {id: $bid})" \
        "MERGE (a)-[:HAS]->(b)"
        self.add_transaction(f"ADD {self.id} {bid}")
        result = tx.run(query, aid=self.id, bid=bid)

    @execute(WRITE)
    def add_transaction(tx, self, log):
        query = "MATCH (i:Identity {id: $id})-[r:IS]->(p:Transaction) " \
        "DELETE r " \
        "MERGE (n:Transaction {log: $log})-[:SUCCEEDS]->(p) " \
        "MERGE (i)-[:IS]->(n)"
        result = tx.run(query, id=self.id, log=log)

    @classmethod
    def new(cls, data):
        identity = cls(nanoid.generate())
        identity.data = data
        identity.create(data)
        return identity

class Knowledge:
    def __init__(self, id):
        self.id = id

    @execute(WRITE)
    def create(tx, self, props):
        query = "CREATE (k:Knowledge {id: $id}) SET k += $props "
        result = tx.run(query, id=self.id, props=props)

    @classmethod
    def new(cls, data):
        knowledge = cls(nanoid.generate())
        knowledge.create(data)
        return knowledge

@execute(WRITE)
def reset(tx):
    query = "MATCH (n) DETACH DELETE (n)"
    tx.run(query)

reset()

k1 = Knowledge.new({'name': 'KOI Identity'})
k2 = Knowledge.new({'name': 'KMS Refactor'})
k3 = Knowledge.new({'name': 'Identity as History'})
k4 = Knowledge.new({'name': 'Meeting Transcript'})


sys = Identity.new({'name': 'sys'})
tag = Identity.new({'name': 'tag'})
type = Identity.new({'name': 'type'})
sys.add_child(tag.id)
sys.add_child(type.id)

kms = Identity.new({'name': 'KMS'})
tag.add_child(kms.id)

hackmd = Identity.new({'name': 'HackMD'})
docs = Identity.new({'name': 'Google Docs'})
type.add_child(hackmd.id)
type.add_child(docs.id)

kms.add_child(k1.id)
kms.add_child(k2.id)
kms.add_child(k3.id)
hackmd.add_child(k1.id)
hackmd.add_child(k2.id)
docs.add_child(k3.id)
docs.add_child(k4.id)

driver.close()