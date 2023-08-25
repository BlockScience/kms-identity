import functools, re, traceback
import jsonschema
from jsonschema.exceptions import ValidationError
from fastapi import HTTPException, status
from api.core import driver
from api.config import NEO4J_DB
from api.exceptions import *

def execute_read(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with driver.session(database=NEO4J_DB) as session:
            return session.execute_read(func, *args, **kwargs)
    return wrapper

def execute_write(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with driver.session(database=NEO4J_DB) as session:
            return session.execute_write(func, *args, **kwargs)
    return wrapper

def pass_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(traceback.format_exc())
            exception_name = type(e).__name__
            raise HTTPException(
                status_code=400,
                detail=f"{exception_name}: {str(e)}"
            )
    return wrapper

def to_snake_case(symbol):
        return re.sub(r"(?<!^)(?=[A-Z])", r"_", symbol).lower()

def to_camel_case(symbol):
    return ''.join(word.title() for word in symbol.split('_'))