from api import transformers
from api.utils import to_camel_case, to_snake_case


def get_transformer(rid):
    means, reference = rid.split(':', 1)
    try:
        transformer = getattr(transformers, to_camel_case(means))
        print(transformer)
        return transformer
    except AttributeError:
        return None
    
# def match()

# rid = "slack:blockscienceteam/C0593RJJ2CW/p1688853562490609"

# transformer = get_transformer(rid)
# reference = transformer.from_rid(rid)
# print(reference)