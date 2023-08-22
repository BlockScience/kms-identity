from . import means
from .core import RID
from .exceptions import *
import inspect

means_classes = [
    m[1] for m in
    inspect.getmembers(means)
    if inspect.isclass(m[1]) and
    issubclass(m[1], RID) and
    m[1] is not RID
]

means_table = {
    m.symbol: m for m in means_classes
}

def lookup(symbol):
    if symbol not in means_table:
        raise MeansNotFoundError(f"No entry for '{symbol}' found in means module")
    else:
        return means_table[symbol]