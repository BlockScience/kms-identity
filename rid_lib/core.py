from rid_lib.exceptions import *
import functools
import jsonschema
from jsonschema.exceptions import ValidationError

class ConstructorAccessMetaClass(type):
    def __getattr__(cls, name):
        try:
            action = cls.actions[name]
        except ValueError:
            raise ActionNotFoundError(f"Action '{name}' undefined for means '{cls.symbol}'")

        def wrapper(ctx=None, **kwargs):
            if not ctx:
                ctx = kwargs
            else:
                ctx.update(kwargs)

            return action(cls, ctx)
        return wrapper

class RID(metaclass=ConstructorAccessMetaClass):
    symbol: str
    label: str
    actions: dict

    def __init__(self, reference):
        self.reference = reference
    
    @property
    def means(self):
        return self.__class__

    @property
    def ref(self):
        return self.reference
    
    @property
    def string(self):
        return str(self)

    def __str__(self):
        return self.symbol + ":" + self.reference
    
    def __repr__(self):
        return f"RID object {(self.symbol, self.reference)}"
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.reference == other.reference
        return False
    
    def __getattr__(self, name):
        try:
            action = self.actions[name]
        except ValueError:
            raise ActionNotFoundError(f"Action '{name}' undefined for means '{self.symbol}'")

        def wrapper(ctx=None, **kwargs):
            if not ctx:
                ctx = kwargs
            else:
                ctx.update(kwargs)

            return action(self, ctx)
        return wrapper
    
def function(constructor=False, schema=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(identifier, context=None):
            if constructor:
                if not isinstance(identifier, type):
                    raise ActionTypeError(f"Unable to call constructor function '{func.__name__}' on a RID object, must be called on the class")
            else:
                if not isinstance(identifier, RID):
                    raise ActionTypeError(f"Unable to call regular function '{func.__name__}' on a RID class, must be called on the object") 
            
            if schema:
                if context is None:
                    raise MissingContextError("Context schema set but no context provided")
                
                try:
                    jsonschema.validate(context, schema)
                except ValidationError as e:
                    raise ContextSchemaValidationError(e.message)
                
            return func(identifier, context)
        return wrapper
    return decorator


# obj = HackMD("uUm16q1oQDmN8T0m9FABNA")

# print(obj.dereference())

# print(obj.transform({"means": "url"}))

# rel = UndirectedRelation.create(
#     name = "Relation",
#     members = [
#         "hackmd:XVaejEw-QaCghV1Tkv3eVQ",
#         "hackmd:y302YrhfRXm64j_51fbEGA",
#         "hackmd:ynez1CzJS6KPRByPzCwhfA"
#     ]
# )

# print(rel)
