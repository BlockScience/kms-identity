import requests
from bs4 import BeautifulSoup

def html(url):
    page = requests.get(url)

    return {
        "text": page.content
    }

def hackmd(url):
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