from ..core import function
from ..schema import TRANSFORMER_CONTEXT_SCHEMA
from ..means import HackMD, Slack

import re, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

@function(schema=TRANSFORMER_CONTEXT_SCHEMA)
def transform_url(rid, context):
    means = context["means"]

    if means == Slack.symbol:
        ref =  re.sub(
            r"^https://(\w+).slack.com/archives/(\w+)/(\w+)$",
            r"\1/\2/\3",
            rid.ref)
        
        return Slack(ref)
    
    elif means == HackMD.symbol:
        return HackMD(urlparse(rid.ref).path[1:])


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