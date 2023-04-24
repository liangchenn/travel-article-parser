from collections import defaultdict

import requests
from bs4 import BeautifulSoup


def parse_url(url: str):

    data = defaultdict(list)
    try:
        resp = requests.get(url, timeout=30)
    except Exception:
        return {}
    soup = BeautifulSoup(resp.content, "lxml")

    level = 1
    while True:
        results = [ele.text for ele in soup.select(f"h{level}")]
        if not len(results):
            break

        data[f"header_{level}"].extend(results)
        level += 1

    return data
