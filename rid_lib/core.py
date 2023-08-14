from rid_lib import utils, exceptions
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

    def __str__(self):
        return utils.compose(self.means, self.reference)
    
    def __repr__(self):
        return f"RID object {(self.means, self.reference)}"
    
    def __eq__(self, other):
        if isinstance(other, RID):
            return (self.means == other.means) and (self.reference == other.reference)
        return False

    @classmethod
    def from_string(cls, rid):
        means, reference = utils.decompose(rid)
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