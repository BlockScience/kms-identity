from rid_lib.exceptions import *
from abc import ABC, abstractmethod
import jsonschema
from jsonschema.exceptions import ValidationError

class RID:
    def __init__(self, means, reference):
        self.means = means
        self.reference = reference

    # alias "ref" for "reference"
    @property
    def ref(self):
        return self.reference
    
    @property
    def string(self):
        return str(self)
    
    @property
    def dict(self):
        return self.__dict__

    def __str__(self):
        return self.means + ":" + self.reference
    
    def __repr__(self):
        return f"RID object {(self.means, self.reference)}"
    
    def __eq__(self, other):
        if isinstance(other, RID):
            return (self.means == other.means) and (self.reference == other.reference)
        return False

    @classmethod
    def from_string(cls, rid_str):
        # only splits on first ":", will include the rest in the second str segment
        components = rid_str.split(":", 1)
        # if there is only one component then there was no means specified
        if len(components) != 2: 
            raise IncompleteRIDError
        
        means, reference = components
        return cls(means, reference)
    
class Means:
    symbol: str
    actions: dict

class Action(ABC):
    context_schema = None

    @classmethod
    def run(cls, rid: RID, context: dict | None = None):
        # if type(rid) is not RID:
        #     raise MissingRIDError

        if cls.context_schema:
            if not context:
                raise MissingContextError("Context schema set but no context provided")

            try:
                jsonschema.validate(context, cls.context_schema)
            except ValidationError as e:
                raise ContextSchemaValidationError(e.message)
            
        return cls.func(rid, context)
    
    @staticmethod
    @abstractmethod
    def func(rid, context):
        raise NotImplementedError
    
class Constructor(ABC):
    context_schema = None

    @classmethod
    def run(cls, means, context: dict | None = None):
        if cls.context_schema:
            if not context:
                raise MissingContextError("Context schema set but no context provided")

            try:
                jsonschema.validate(context, cls.context_schema)
            except ValidationError as e:
                raise ContextSchemaValidationError(e.message)
        
        return cls.func(means, context)

    @staticmethod
    @abstractmethod
    def func(cls, context):
        raise NotImplementedError