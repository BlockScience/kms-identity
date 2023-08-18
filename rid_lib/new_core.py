from rid_lib.functions import *

class NewRID:
    means: str
    actions: dict

    def __init__(self, reference):
        self.reference = reference

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
    
    def __getattr__(self, name):
        action = self.actions[name]

        def func(ctx=None):
            return action.run(self, ctx)
        
        return func
    
class HackMD(NewRID):
    symbol = "hackmd"
    actions = {
        "dereference": DereferenceHackmd,
        "transform": TransformHackmd
    }

obj = HackMD("uUm16q1oQDmN8T0m9FABNA")

print(obj.dereference())
print(obj.transform({"means": "url"}))