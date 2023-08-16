from rid_lib.core import Action, RID
from rid_lib.schema import TRANSFORMER_CONTEXT_SCHEMA

import re, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class TransformUrl(Action):
    symbol = "transform_url"
    needs_context = True
    context_schema = TRANSFORMER_CONTEXT_SCHEMA

    @staticmethod
    def func(rid, context):
        means = context["means"]

        if means == "slack":
            ref =  re.sub(
                r"^https://(\w+).slack.com/archives/(\w+)/(\w+)$",
                r"\1/\2/\3",
                rid.ref)
            
            return RID("slack", ref)
        
        elif means == "hackmd":
            ref = urlparse(rid.ref).path[1:]
            return RID("hackmd", ref)


class DereferenceUrl(Action):

    @staticmethod
    def func(rid):
        page = requests.get(rid.ref)
        page.raise_for_status()

        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.find(name="title").get_text()
        text = soup.find(name="body").get_text(" ")

        return {
            "title": title,
            "text": text
        }

table = {
    "transform": TransformUrl,
    "dereference": DereferenceUrl
}