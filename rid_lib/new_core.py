from rid_lib.functions import *

class ConstructorMetaClass(type):
    def __getattr__(cls, name):
        action = cls.actions[name]

        def func(ctx=None, **kwargs):
            if ctx is None:
                ctx = kwargs
            else:
                ctx.update(kwargs)

            return action.run(cls, ctx)
        
        return func

class NewRID(metaclass=ConstructorMetaClass):
    means: str
    label: str
    actions: dict

    def __init__(self, reference):
        self.reference = reference

    @property
    def ref(self):
        return self.reference
    
    @property
    def means(self):
        return self.symbol
    
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

        def func(ctx=None, **kwargs):
            if not ctx:
                ctx = kwargs
            else:
                ctx.update(kwargs)

            return action.run(self, ctx)
        
        return func
    
class HackMD(NewRID):
    symbol = "hackmd"
    actions = {
        "dereference": DereferenceHackmd,
        "transform": TransformHackmd
    }

class UndirectedRelation(NewRID):
    symbol = UNDIRECTED_RELATION
    actions = {
        "create": CreateUndirectedRelation,
        "read": ReadRelation,
        "delete": DeleteRelation
    }

obj = HackMD("uUm16q1oQDmN8T0m9FABNA")

print(obj.dereference())
print(obj.transform({"means": "url"}))

rel = UndirectedRelation.create(
    name = "Relation",
    members = [
        "hackmd:XVaejEw-QaCghV1Tkv3eVQ",
        "hackmd:y302YrhfRXm64j_51fbEGA",
        "hackmd:ynez1CzJS6KPRByPzCwhfA"
    ]
)

print(rel)
