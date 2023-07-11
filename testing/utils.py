import functools
from neo4j import GraphDatabase

URI = "neo4j+s://677dd1d2.databases.neo4j.io"
AUTH = ("neo4j", "_5oVUUBXGjb-1qUhHsd5ucKe5v27odqjWvt5wouNqSo")

driver = GraphDatabase.driver(URI, auth=AUTH)

READ = "read"
WRITE = "write"

def execute(mode, db="neo4j"):
    def execute_internal(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            with driver.session(database=db) as session:
                if mode == READ:
                    result = session.execute_read(method, *args, **kwargs)
                elif mode == WRITE:
                    result = session.execute_write(method, *args, **kwargs)
                return result
        return wrapper
    return execute_internal

def exit():
    driver.close()