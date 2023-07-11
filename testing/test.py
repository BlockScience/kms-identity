from neo4j import GraphDatabase

class Test:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print(self, message):
        with self.driver.session() as session:
            greet = session.execute_write(
                self.greeting,
                message
            )
            print(greet)
    
    @staticmethod
    def greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)",
                        message=message)
        return result.single()[0]

greeter = Test("bolt://localhost:7687", "neo4j", "12345678")
greeter.print('hello_world')
greeter.close()