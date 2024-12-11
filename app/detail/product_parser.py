"""Product detail parsing."""

from bs4 import Tag  # type: ignore
from typing import Tuple, Dict, Any


class S:
    """html tag selectors."""

    him_div_id = "him_bx"  # химический состав, пищевая ценность
    him_p_at_end = "pr__ind_endline"  # суммарное содержание

    f_span = "pr__fat"  # жиры
    p_span = "pr__protein"  # белки
    c_span = "pr__carbohydrate"  # углеводы
    w_span = "pr__water"  # вода
    a_span = "pr__ash"  # зола


def _get_quantity(s: Tag) -> Tuple[float, str]:
    while s.name != "span":
        s = s.next
        continue
    t = s.text.replace(",", ".")
    v, u = t.split()
    return float(v), u


def _product_info_parser(soup: Any) -> Dict:
    him = soup.find("div", id=S.him_div_id)
    product: Dict = {}

    # content
    product.update({"content": {}})
    content = product.get("content", {})
    content.update(
        {
            "sentence": him.p.get_text("|", strip=True),
            "f": _get_quantity(him.find_next("span", class_=S.f_span).next),
            "p": _get_quantity(him.find_next("span", class_=S.p_span).next),
            "c": _get_quantity(him.find_next("span", class_=S.c_span).next),
            "w": _get_quantity(him.find_next("span", class_=S.w_span).next),
            "a": _get_quantity(him.find_next("span", class_=S.a_span).next),
        }
    )

    him_summary, him_bju_daily, him_vitamins, him_minerals = him.find_next_siblings("p")

    # summary
    product.update({"summary": {}})
    summary = product.get("summary", {})
    summary.update({"sentence": him_summary.get_text("|", strip=True)})
    for a in him_summary.find_all("a"):
        n = a.get_text()
        v = a.next.next.next.get_text()
        summary.update({n: v})

    # bju daily percent
    product.update({"daily": {}})
    daily = product.get("daily", {})
    daily.update({"sentence": him_bju_daily.get_text("|", strip=True)})
    bju_tbl = him_bju_daily.findNext("table")
    for i, r in enumerate(bju_tbl.find_all("tr")):
        if i == 0:
            continue
        name, q, u, norm_perc = r.get_text().strip().split()
        daily.update({name: (q, u, norm_perc)})

    # him_vitamins
    product.update({"vitamins": {}})
    vitamins = product.get("vitamins", {})
    vitamins.update({"sentence": him_vitamins.get_text("|", strip=True)})
    bju_tbl = him_vitamins.findNext("table")
    for i, r in enumerate(bju_tbl.find_all("tr")):
        if i == 0:
            continue
        heap = r.get_text().strip().split()
        norm_perc = heap.pop()
        u = heap.pop()
        q = heap.pop()
        name = "".join(heap)

        vitamins.update({name: (name, q, u, norm_perc)})

    # him_minerals
    product.update({"minerals": {}})
    minerals = product.get("minerals", {})
    minerals.update({"sentence": him_minerals.get_text("|", strip=True)})
    bju_tbl = him_minerals.findNext("table")
    for i, r in enumerate(bju_tbl.find_all("tr")):
        if i == 0:
            continue
        name, *q, norm_perc = r.get_text().strip().split()
        q = q if len(q) > 1 else (q[0], "-")
        minerals.update({name: (*q, norm_perc)})

    return product
