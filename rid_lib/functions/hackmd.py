from ..core import function
from ..schema import TRANSFORMER_CONTEXT_SCHEMA
from ..means import URL
import requests
from bs4 import BeautifulSoup

@function(schema=TRANSFORMER_CONTEXT_SCHEMA)
def transform_hackmd(rid, context):
    means = context["means"]

    if means == URL.symbol:
        return URL("https://hackmd.io/" + rid.reference)


@function()
def dereference_hackmd(rid, context):
    url_rid = rid.transform(means=URL.symbol)
    url = url_rid.reference

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