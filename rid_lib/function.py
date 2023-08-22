from .core import function
from .schema import TRANSFORMER_CONTEXT_SCHEMA
from .means import Url
from api.schema import *
import nanoid, requests
import api
from bs4 import BeautifulSoup

@function(constructor=True, schema=UNDIRECTED_RELATION_SCHEMA)
def create_undirected_relation(RID, context):
    rid = RID(nanoid.generate())
    api.database.create_undirected_relation(rid, context)
    return rid

@function()
def read_relation(rid, context):
    return api.database.read_relation(rid)

@function()
def delete_relation(rid, context):
    api.database.delete_relation(rid)

@function(schema=TRANSFORMER_CONTEXT_SCHEMA)
def transform_hackmd(rid, context):
    means = context["means"]

    if means == "url":
        return Url("https://hackmd.io/" + rid.ref)

@function()
def dereference_hackmd(rid, context):
    url_rid = rid.transform(means="url")
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