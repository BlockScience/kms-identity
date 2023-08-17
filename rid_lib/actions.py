from . import means, Means
from .exceptions import *
import inspect

# gets all of the 'Means' classes from the means module
means_classes = [
    m[1] for m in
    inspect.getmembers(means)
    if inspect.isclass(m[1]) and
    issubclass(m[1], Means) and
    m[1] is not Means
]

table = {
    m.symbol: m for m in means_classes
}

def lookup(means, action):
    if means not in table:
        raise MeansNotFoundError(f"No entry for '{means}' found in means module")
    
    m = table[means]

    if action not in m.actions:
        raise ActionNotFoundError(f"No entry for '{action}' found in '{means}' action table")
    
    action = m.actions[action]

    return action