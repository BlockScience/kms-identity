from rid_lib.core import ContextualAction, Action, RID
from rid_lib.schema import TRANSFORMER_CONTEXT_SCHEMA

import requests
from bs4 import BeautifulSoup

class TransformHackmd(ContextualAction):
    context_schema = TRANSFORMER_CONTEXT_SCHEMA

    @staticmethod
    def func(rid, context):
        means = context["means"]

        if means == "url":
            ref = "https://hackmd.io/" + rid.ref
            return RID("url", ref)

class DereferenceHackmd(Action):

    @staticmethod
    def func(rid):
        url_rid = TransformHackmd.run(rid, context={"means": "url"})
        url = url_rid.ref

        page = requests.get(url)

        try:
            page.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f"could not get HackMD URL ({url})", page.status_code)
            return None

        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.find(name="title").get_text()
        source = soup.find(id="doc") or soup.find("div", class_="slides")
        text = source.get_text()
        if title.endswith(' - HackMD'):
            title = title[:-9]

        return {
            "title": title,
            "text": text
        }