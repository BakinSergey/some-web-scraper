"""scrape page of Product detail."""

import asyncio
from queue import Queue

from app import product_path, product_soup
from app.detail.product_parser import _product_info_parser
from app.utils.soup import get_soup_from_http


async def _update_products(q: Queue, products: dict[int, dict]) -> None:
    while True:
        (id_, rich_info) = await q.get()
        products.get(id_).update(rich_info)
        q.task_done()
        print(id_)


async def _get_product_richup_info(in_q, out_q, session) -> None:
    while True:
        id_ = await in_q.get()
        soup_url = product_path.format(id_)
        soup_name = product_soup.format(id_)

        soup = await get_soup_from_http(soup_url, soup_name, session)

        rich_info = await asyncio.to_thread(_product_info_parser, soup)
        await out_q.put((id_, rich_info))

        in_q.task_done()
