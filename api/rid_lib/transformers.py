import re
from urllib.parse import urlparse

def re_transform(pattern, replace):
    def transform(ref):
        return re.sub(pattern, replace, ref)
    return transform

def url_to_hackmd(url):
    return urlparse(url).path[1:]

def hackmd_to_url(id):
    return f"https://hackmd.io/{id}"

table = {
    ("url", "slack"): re_transform(
        r"^https://(\w+).slack.com/archives/(\w+)/(\w+)$",
        r"\1/\2/\3"
    ),
    ("slack", "url"): re_transform(
        r"^(\w+)/(\w+)/(\w+)$",
        r"https://\1.slack.com/archives/\2/\3"
    ),
    ("url", "hackmd"): url_to_hackmd,
    ("hackmd", "url"): hackmd_to_url
}

"https://{team}.slack.com/archives/{channel}/{message}"

"slack:blockscienceteam/C0593RJJ2CW/p1688853562490609"