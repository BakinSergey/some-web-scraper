"""Nutrient detail parsing."""

from bs4 import BeautifulSoup


def _nutrient_info_parser(soup: BeautifulSoup):
    tbl = soup.find("table")

    nutrient = {}
    products = []

    for i, tr in enumerate(tbl.tbody.find_all("tr")):
        if i == 0:
            continue
        heap = tr.get_text().strip().split()
        prod_id = int(tr.find_next("a")["href"].split("/")[-1])

        u = heap.pop()
        q = heap.pop()

        products.append({prod_id: (q, u)})
    nutrient.update({"products": products})
    return nutrient
