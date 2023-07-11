from neo4j import GraphDatabase
import nanoid

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "identity")

driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

def create_identity(tx, name, description):
    _id = nanoid.generate()
    result = tx.run(
        "CREATE (i:Identity {name: $name, id: $_id}) RETURN i",
        name=name, _id=_id
    )
    print(f"Created new identity: '{name}' [{_id}]")
    return list(result)


def query_nodes(tx):
    result = tx.run(
        "MATCH (n) RETURN n"
    )
    return result.graph()

with driver.session(database='neo4j') as session:
    people = session.execute_write(create_identity, name="Luke", description="Pretty cool dude :)")
    print(people)
    # nodes = session.execute_write(query_nodes)
    # print(nodes)
driver.close()