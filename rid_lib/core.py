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
    symbol: None
    actions: dict


class Action(ABC):
    requires_rid = True
    requires_context = False
    context_schema = None

    @classmethod
    def run(cls, rid=None, context=None):
        if cls.requires_rid:
            if not rid:
                raise MissingRIDError
        else:
            return cls.func()

        if cls.requires_context:
            if not context:
                raise MissingContextError
            
            if not cls.context_schema:
                raise MissingContextSchemaError
            
            try:
                jsonschema.validate(context, cls.context_schema)
            except ValidationError as e:
                raise ContextSchemaValidationError(e.message)

            return cls.func(rid, context)
        return cls.func(rid)

    @staticmethod
    @abstractmethod
    def func(rid, context):
        raise NotImplementedError
    
class ContextualAction(Action):
    requires_context = True

class ConstructorAction(Action):
    requires_rid = False