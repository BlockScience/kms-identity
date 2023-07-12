import functools
import jsonschema
from jsonschema.exceptions import ValidationError
from fastapi import HTTPException, status
from api.core import driver
from api.config import NEO4J_DB

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

def validate_json(schema, instance=None):
    """Decorator to validate JSON body. Uses first kwarg by default, can be overidden by setting instance to the name of the kwarg you want to use."""
    def decorator(func):
        # if using async fastapi functions, wrapper will need to be async as well
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(args, kwargs)

            nonlocal instance

            if not instance:
                instance = next(iter(kwargs.keys()), None)

            if not instance:
                raise Exception("Instance is missing from function params")

            if instance not in kwargs:
                raise Exception(f"Instance name '{instance}' not found in function params")

            if type(kwargs[instance]) is not dict:
                raise Exception("Instance is not of type 'dict'")
            
            try:
                jsonschema.validate(kwargs[instance], schema)
            except ValidationError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator