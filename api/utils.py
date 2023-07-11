import functools
from api.core import driver
from api.config import NEO4J_DB

def execute_read(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        with driver.session(database=NEO4J_DB) as session:
            return session.execute_read(method, *args, **kwargs)
    return wrapper

def execute_write(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        with driver.session(database=NEO4J_DB) as session:
            return session.execute_write(method, *args, **kwargs)
    return wrapper
