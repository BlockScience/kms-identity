from rid_lib import utils

class RID:
    def __init__(self, means, reference):
        self.means = means
        self.reference = reference

    def __str__(self):
        return utils.compose(self.means, self.reference)

    @classmethod
    def from_string(cls, rid):
        means, reference = utils.decompose(rid)
        return cls(means, reference)

class Action:
    needs_context = False
    context_schema = None
    supported_means = []

    def __init__(self):
        ...

    def run(self, rid: RID, context=None):
        if self.needs_context and not context:
            ...
            
