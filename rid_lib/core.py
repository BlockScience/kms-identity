from rid_lib import exceptions
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
            raise exceptions.MissingMeansError()
        
        means, reference = components
        return cls(means, reference)

class Action:
    needs_context = False
    context_schema = None
    supported_means = []
    action_type = None

    @classmethod
    def run(cls, rid: RID, context=None):
        if rid.means not in cls.supported_means:
            raise exceptions.UnsupportedMeansError

        if cls.needs_context:
            if not context:
                raise exceptions.MissingContextError
            
            if not cls.context_schema:
                raise exceptions.MissingContextSchemaError
            
            try:
                jsonschema.validate(context, cls.context_schema)
            except ValidationError as e:
                raise exceptions.ContextSchemaValidationError(e.message)

            return cls.func(rid, context)
        return cls.func(rid)

    @staticmethod
    def func(cls, rid: RID, context):
        ...