from abc import ABC
from urllib.parse import urlparse
import re

# def match(symbol):


class Transformer:
    pattern_ref = None
    replace_ref = None
    pattern_rid = None
    replace_rid = None

    @classmethod
    def to_rid(cls, ref):
        rid = re.sub(cls.pattern_ref, cls.replace_ref, ref)
        return rid
    
    @classmethod
    def from_rid(cls, rid):
        ref = re.sub(cls.pattern_rid, cls.replace_rid, rid)
        return ref
    
class Url(Transformer):
    pattern_ref = r"^(https?:\/\/[^\s/$.?#].[^\s]*)$"
    replace_ref = r"\1"
    pattern_rid = r"(.+)"
    replace_rid = r"\1"
    default_dereferencer = "html"

class Slack(Transformer):
    pattern_ref = r"^https://(\w+).slack.com/archives/(\w+)/(\w+)$"
    replace_ref = r"\1/\2/\3"
    pattern_rid = r"^(\w+)/(\w+)/(\w+)$"
    replace_rid = r"https://\1.slack.com/archives/\2/\3"

    



# replacement = r"slack:\1/\2/\3"
# rid = re.sub(pattern, replacement, url)
# print(rid)

# class HackMD:
#     scheme = 'hackmd'


    


"https://{team}.slack.com/archives/{channel}/{message}"

"slack:blockscienceteam/C0593RJJ2CW/p1688853562490609"