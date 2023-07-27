from api.rid_lib import transformers

# get_prefix flag indicates whether input is an rid (means:reference) or just a reference
# set_prefix flag indicates whether output should be an rid or reference
def transform(r, transformation, get_prefix=False, set_prefix=True):
    from_means, to_means = transformation
    
    if transformation not in transformers.table:
        return None
    
    transformer = transformers.table[transformation]

    if get_prefix:
        means, reference = decompose(r)
        if means != from_means:
            raise Exception(f"Mismatch between inputted means of reference '{means}' and transformation from means of reference '{from_means}'")
    else:
        reference = r

    new_reference = transformer(reference)
    
    if set_prefix:
        return compose(to_means, new_reference)
    else:
        return new_reference


def decompose(rid):
    components = rid.split(":", 1)
    if len(components) != 2: return False
    return tuple(components)

def compose(means, reference):
    return f"{means}:{reference}"