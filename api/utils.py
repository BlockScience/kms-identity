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

def validate_json(schema, instance=None):
    """Decorator to validate JSON body. Uses first kwarg by default, can be overidden by setting instance to the name of the kwarg you want to use."""
    def decorator(func):
        # if using async fastapi functions, wrapper will need to be async as well
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal instance

            if not instance:
                instance = next(iter(kwargs.keys()), None)

            if not instance:
                raise MissingInstanceError

            if instance not in kwargs:
                raise InstanceNotFoundError(f"Instance name '{instance}' not found in function params")

            if type(kwargs[instance]) is not dict:
                raise InstanceValueError("Instance is not of type 'dict'")
            
            try:
                jsonschema.validate(kwargs[instance], schema)
            except ValidationError as e:
                print(e.message)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e.message
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def to_snake_case(symbol):
        return re.sub(r"(?<!^)(?=[A-Z])", r"_", symbol).lower()

def to_camel_case(symbol):
    return ''.join(word.title() for word in symbol.split('_'))