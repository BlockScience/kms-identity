from api import transformers, dereferencers
from api.utils import to_camel_case, to_snake_case

def retrieve(rid):
    means, identifier = rid.split(':', 1)
    transformer_name, *other = means.split('+', 1)
    dereferencer_name = other[0] if other else None

    try:
        transformer = getattr(transformers, to_camel_case(transformer_name))
    except AttributeError:
        raise Exception(f"Transformer '{transformer_name}' not found")
    
    reference = transformer.from_rid(identifier)
    print(reference)
    
    if not dereferencer_name:
        try:
            dereferencer_name = transformer.default_dereferencer
        except AttributeError:
            raise Exception(f"Transformer '{transformer_name}' did not have a default dereferencer and none was specified")
    
    try:
        dereference = getattr(dereferencers, dereferencer_name)
    except AttributeError:
        raise Exception(f"Dereferencer '{dereferencer_name}' not found")
    
    
    data = dereference(reference)

    return data
    


# def get_dereferencer(ref):

"slack+poll:https://block.science"
"url+hackmd:"

    
# def match()

# rid = "slack:blockscienceteam/C0593RJJ2CW/p1688853562490609"

# transformer = get_transformer(rid)
# reference = transformer.from_rid(rid)
# print(reference)