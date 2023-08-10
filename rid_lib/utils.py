from rid_lib import transformers, actions


def transform(r, from_=None, to=None, return_rid=True):
    if from_:
        from_means = from_
        reference = r
    else:
        # assume input is rid and infer from_means
        from_means, reference = decompose(r)
    
    transformer = transformers.table.get((from_means, to), None)

    if not transformer:
        raise Exception(f"Transformer for '{from_means}' -> '{to}' not found")

    new_reference = transformer(reference)
    
    if return_rid:
        return compose(to, new_reference)
    else:
        return new_reference

def dereference(rid):
    means, reference = decompose(rid)

    action = actions.table.get(means, None)
    if not action: 
        raise Exception(f"No action found for means '{means}'")
    
    data = action(rid)
    return data

def decompose(rid):
    components = rid.split(":", 1)
    if len(components) != 2: return False
    return tuple(components)

def compose(means, reference):
    return f"{means}:{reference}"