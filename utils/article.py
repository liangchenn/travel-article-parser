from collections import defaultdict

import requests
from bs4 import BeautifulSoup


def parse_url(url: str):

    data = defaultdict(list)

    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "lxml")

    level = 1
    while True:
        results = [ele.text for ele in soup.select(f"h{level}")]
        if not len(results):
            break

        data[f"header_{level}"].extend(results)
        level += 1

    return data
