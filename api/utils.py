from api.core import driver

def new_transaction(tx, *args, **kwargs):
    print(args, kwargs)
    # print(query, kwargs)
    # result = tx.run(query, **kwargs)
    # return list(result)

def run_transaction(method, *args, **kwargs):
    with driver.session(database="neo4j") as session:
        result = session.execute_write(method, *args, **kwargs)
        return result