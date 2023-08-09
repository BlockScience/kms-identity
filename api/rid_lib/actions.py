from api.rid_lib import utils

import requests
from bs4 import BeautifulSoup

def test_action(rid):
    means, ref = utils.decompose(rid)
    return {
        "data": ref
    }

def generic_url(url):
    page = requests.get(url)
    page.raise_for_status()

    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(name="title").get_text()
    text = soup.find(name="body").get_text(' ')

    return {
        "title": title,
        "text": text
    }

def extract_hackmd(rid):
    url = utils.transform(rid, to="url", return_rid=False)
    page = requests.get(url)

    try:
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        return f"could not get HackMD URL ({url})", page.status_code

    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(name="title").get_text()
    source = soup.find(id="doc") or soup.find("div", class_="slides")
    text = source.get_text()
    if title.endswith(' - HackMD'):
        title = title[:-9]

    data = {
        "title": title,
        "text": text
    }

    return data

table = {
    "url": generic_url,
    "hackmd": extract_hackmd,
    "test": test_action
}
