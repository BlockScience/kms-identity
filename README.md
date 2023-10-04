# RID system

The Reference Identifier (RID) system is a flexible way of referring to and interacting with knowledge objects. RIDs are designed to support objects that are external to but "observed" by the system. They can be thought of a similar to pointers in a low level programming langauge that store the memory location of data, rather than the data itself. In the same way, RIDs can be "dereferenced" to retrieve the data associated with a particular object.

An RID is composed of two parts, a means of reference (or just "means") and the reference itself, separated by a colon, `means:reference`. The means tells us what kind of object an RID is referring to, the actions associated with it, and provides distinction for two RIDs with the same reference (ie the same username on two different platforms). The reference uniquely identifies an object under a specific means. For some means, this could act as a location that describes where to find the data, but it could also just be an identifier.


## Means

In the Python implementation, means are represented as a class and instances of that class are RIDs. The built in Python constructor is used to create an RID from a means class and a reference string. 

```python
rid = Means(reference)
rid = URL("https://block.science")
```

An RID object does not store any additional information, and can always be reconstructed from a string. The string representation can be accessed by `str(rid)` or `rid.string`. The means class can be accessed with `rid.means` and its symbol (string representation) can be accessed with `rid.means.symbol`. To create a new means class, you simply need to inherit from the `Object` class, or an existing means class, and define its symbol.


```python
# (in rid_lib/means.py)

class URL(Object):
    symbol = "url"
```


### Actions

The other main component of a means are associated actions. These are functions that operate on, with, or using an RID in some way. They are bound with a name to a means to define the action space of RIDs under a certain means.

In the Python implementation, these are class and instance methods of a means class. They can be accessed using the dot operator just like a regular class.

```python
document = HackMD("yBdb2NKoRsimv7NH1T384Q")
print(document.dereference())
```

Action functions take in two parameters, the RID itself and an optional context dict. The context can also be validated by a JSON schema to ensure certain expected fields. When calling an action on an RID, context can be passed as a dictionary, key word arguments, or a mix of both.

```python
page = URL("https://hackmd.io/yBdb2NKoRsimv7NH1T384Q")
document = page.transform(means="hackmd")
document = page.transform({"means": "hackmd"})
```

There is also a special type of action called a constructor. Unlike regular actions, constructors do not take an RID as input, and are instead passed the means class with an optional context. The primary use case is to create and return a new RID object, but constructors aren't just limited to this.

```python
# note this action is combining a dict and kwargs to pass in the context
relation = UndirectedRelation.create(
    {
        "name": "KMS",
        "description": "A tag for knowledge objects related to Knowledge Management Systems"
    },
    members=["hackmd:uUm16q1oQDmN8T0m9FABNA", "hackmd:M2IWdXC_S_OSUHA6zkYFYw"]
)
```

Actions start as unbound functions defined by a decorator with two optional parameters defaulting to `@function(constructor=False, schema=None)`. Here are two examples of function definitions:

```python
@function()
def dereference_url(rid, context):
    page = requests.get(rid.ref)
    page.raise_for_status()

    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(name="title").get_text()
    text = soup.find(name="body").get_text(" ")

    return {
        "title": title,
        "text": text
    }
```

```python
@function(
    constructor=True,
    schema={
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
)
def create_agent(Means, context):
    name = context.get("name")
    rid = Means(name)
    database.assertions.create_undirected(rid, context)
    return rid
```

Finally in order to become actions, functions are bound to a means class allowing RIDs of that type to call them. Means will inherit all actions defined by their parent class, but can override them by setting an action with same name, or remove them by setting that name to `None`.

```python
# (in rid_lib/actions.py)

HackMD.set_actions({
    "transform": transform_url,
    "dereference": dereference_url
})
```

### Creating new means and actions

New means can easily be created by modifying `rid_lib/means.py` with a new class. It will need to inherit from either `Object` or an existing means class and set a new unique symbol. New actions can be added by modifying `rid_lib/actions.py` and calling `set_actions` on your means class. This function accepts a dict with the action name as the key and the function definition as the value. All functions are located in `rid_lib/functions` and are roughly sorted by means. You can add a new module here with `from ..core import function` to get the needed decorator. Make sure to add this module to the function package by adding `from .module_name import *` to `rid_lib/functions/__init__.py`. 

New means will automatically be available in the API endpoints, from the means module, and through the `Object.from_string` constructor.

### Base Object

All means classes derive from the `Object` base class, which defines a few default actions and the behavior of a means class in Python. (This class is not intended to be used as a literal means, and it doesn't define RIDs of the form `object:reference`). The default actions are: `from_string`, `observe`, `exists`, `read`, and `refresh`.

`Object.from_string(rid=rid_string)` is a special constructor that takes in a full RID string and returns an instance of the proper class based on the means component of the string. If there is no means class defined, it will create a temporary class deriving from the `Object` class. The `from_string` action is inherited by all means, but when calling it on a class besides `Object`, it will only be valid if the means in the string matches the symbol of the class.

The rest of the actions are not constructors, and define default behavior for external objects. For example, `observe` adds the RID as an object node in the neo4j graph, attempts to run `dereference` action and stores the result as a data node. Similarly, `refresh` updates the data node, `read` returns the data it has stored, and `exists` returns whether the RID has been observed as an object node in the system.

## Identity Primitives

As part of this project, four primitive structural means have been defined for internal and external use. They are divided across two categories: relations and assertions, and directed and undirected. All of these structures define the relationship between knowledge objects in the system (including other relations). All structures can also optionally define a definition object that gives additional context on what the structure represents.

Undirected structures are simply a set of member objects.

Directed structures are a mapping *from* one group *to* another group of member objects.

Relations are immutable, they can only be created, read, and deleted.

Assertions are mutable, they can update their properties, definition, and members. They also store a complete record of their changes in a transaction change, allowing assertions to be forked.

Next, we'll show how to perform each action for each type of structure. (If only one example is given, the action works the same for all given structures).

### Create

```python
from rid_lib.means import *

undirected_relation = UndirectedRelation.create({
    "name": "Undirected",
    "definition": "definition:one",
    "members": ["example:one", "example:two", "example:three"]
})

directed_relation = DirectedRelation.create({
    "name": "Directed",
    "definition": "definition:one",
    "from": ["example:one"],
    "to": ["example:two"]
})

undirected_assertion = UndirectedAssertion.create({
    "name": "Undirected",
    "definition": "definition:one",
    "members": ["example:one", "example:two", "example:three"]
})

directed_assertion = DirectedAssertion.create({
    "name": "Directed",
    "definition": "definition:one",
    "from": ["example:one"],
    "to": ["example:two"]
})
```

### Read
```python
print(undirected_relation.read())
```

### Delete
```python
directed_relation.delete()
```

### Update (Assertion only)
```python
undirected_assertion.update(name="Undirected Assertion")
```

### Update Definition (Assertion only)
```python
directed_assertion.update_definition({
    "definition": "definition:two"
})
```

### Update Members (Assertion only)
```python
undirected_assertion.update_members({
    "add": ["example:four"],
    "remove": []"example:one"]
})

directed_assertion.update_members({
    "add": {
        "from": ["example:four", "example:five"],
        "to": ["example:six"]
    },
    "remove": {
        "from": ["example:one"],
        "to": ["example:two", "example:three"]
    }
})
```

### Fork (Assertion only)
```python
new_assertion = undirected_assertion.fork()
```

## API

The API provides a lightweight wrapper around the RID system, with a few different ways of calling actions on objects. The first approach is the most "RESTful" and provides a unique endpoint for each object to perform actions on. One problem with this approach is that RIDs containing URLs can cause parsing errors for the API. To circumvent this, you can also pass the RID in a URL safe base 64 encoded form, with the query param "use_base64=true". Both of these approaches need to pass the optional context as a JSON body.

```
POST /object/{rid}/{action}
```

```
POST /object/{base64_rid}/{action}?use_base64=true
```

The other approach is purely done in the JSON body without the RID or action in the path. 

```
POST /object

{
    "rid": "",
    "action": "",
    "context": {}
}
```



Constructor actions can be called by passing just the means in the RID field. For example, to create a new assertion you would call:

```
POST /object/und_asrt/create

{
    "name": "KOI Development Team",
    "members": [
        "agent:luke",
        "agent:orion",
        "agent:david"
    ]
}
```
Which would return the RID string of the newly created relation, allowing other actions to be called on it.

