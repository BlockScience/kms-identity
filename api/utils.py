import functools, re, traceback
from fastapi import HTTPException
from api.exceptions import *

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