from rid_lib.functions import *
from rid_lib.exceptions import *
from rid_lib.schema import *
import functools
import jsonschema
from jsonschema.exceptions import ValidationError

class ConstructorMetaClass(type):
    def __getattr__(cls, name):
        action = cls.actions[name]

        def func(ctx=None, **kwargs):
            if ctx is None:
                ctx = kwargs
            else:
                ctx.update(kwargs)

            return action(cls, ctx)
        
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

            return action(self, ctx)
        
        return func
    
def function(schema=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(rid, context=None):
            if schema:
                if context is None:
                    raise MissingContextError("Context schema set but no context provided")
                
                try:
                    jsonschema.validate(context, schema)
                except ValidationError as e:
                    raise ContextSchemaValidationError(e.message)

            return func(rid, context)
        return wrapper
    return decorator

def constructor(schema=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(means, context=None):
            if schema:
                if context is None:
                    raise MissingContextError("Context schema set but no context provided")
                
                try:
                    jsonschema.validate(context, schema)
                except ValidationError as e:
                    raise ContextSchemaValidationError(e.message)

            return func(means, context)
        return wrapper
    return decorator

@function
def dereference_hackmd(rid, context):
    url = "https://hackmd.io/" + rid.reference

    page = requests.get(url)

    try:
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"could not get HackMD URL ({url})", page.status_code)
        return None

    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(name="title").get_text()
    source = soup.find(id="doc") or soup.find("div", class_="slides")
    text = source.get_text()
    if title.endswith(' - HackMD'):
        title = title[:-9]

    return {
        "title": title,
        "text": text
    }


class HackMD(NewRID):
    symbol = "hackmd"
    actions = {
        "dereference": dereference_hackmd,
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
