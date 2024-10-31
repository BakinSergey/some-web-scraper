"""Scrape Products Page."""

import asyncio
from asyncio import Queue

from aiohttp import ClientSession
from bs4 import BeautifulSoup as Soup

from app import products_json, products_path, products_soup
from app.detail.product import _get_product_richup_info, _update_products
from app.utils.a_json import save_json
from app.utils.soup import get_soup_from_http
from app.utils.tasks import cancel_tasks, create_tasks


async def eat(soup: Soup, q: Queue):
    """Parse Soup."""
    mains = soup.find_all("section")

    group_items_div_cls = "fimlist__title"
    products = {}

    for t in mains[0].find_all_next("div", class_=group_items_div_cls):
        section_title = t.text.strip().lower()
        section_ul = t.find_next("ul")
        ul_li = section_ul.find_all("li")
        for li in ul_li:
            product = {}
            id_ = int(li.a["href"].strip().split("/")[-1])
            product.update(
                {
                    "category": section_title,
                    "title": li.a["title"].strip(),
                }
            )

            products.update({id_: product})

            await q.put(id_)

    return products


async def scrape_products(session: ClientSession, save: bool) -> int:
    """Scrape Products Page."""
    to_rich_q = asyncio.Queue()
    rich_out_q = asyncio.Queue()

    soup = await get_soup_from_http(products_path, products_soup, session)
    products = await eat(soup, to_rich_q)

    n = 50
    # parse products detail view tasks
    product_getters = create_tasks(
        n, _get_product_richup_info, to_rich_q, rich_out_q, session
    )

    # uprich products data tasks
    product_updater = create_tasks(2, _update_products, rich_out_q, products)

    await to_rich_q.join()
    cancel_tasks(product_getters)

    await rich_out_q.join()
    cancel_tasks(product_updater)

    if save:
        await save_json(products_json, products)

    return len(products)
