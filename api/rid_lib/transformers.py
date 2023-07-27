import re

def re_transform(pattern, replace):
    def transform(ref):
        return re.sub(pattern, replace, ref)
    return transform

URL_TO_SLACK = ("url", "slack")
SLACK_TO_URL = ("slack", "url")

table = {
    ("url", "slack"): re_transform(
        r"^https://(\w+).slack.com/archives/(\w+)/(\w+)$",
        r"\1/\2/\3"
    ),
    ("slack", "url"): re_transform(
        r"^(\w+)/(\w+)/(\w+)$",
        r"https://\1.slack.com/archives/\2/\3"
    )
}

"https://{team}.slack.com/archives/{channel}/{message}"

"slack:blockscienceteam/C0593RJJ2CW/p1688853562490609"