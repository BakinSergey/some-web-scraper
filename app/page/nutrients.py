"""Scrape Nutrients Page."""

import asyncio
from asyncio import Queue

from aiohttp import ClientSession
from bs4 import BeautifulSoup as Soup

from app import (
    NUTRIENTS_TO_SKIP,
    nutrients_json,
    nutrients_path,
    nutrients_soup,
)
from app.detail.nutrient import get_nutrient_richup_info, update_nutrient
from app.utils.a_json import save_json
from app.utils.soup import get_soup_from_http
from app.utils.tasks import cancel_tasks, create_tasks


async def eat(soup: Soup, q: Queue):
    """Parse soup."""
    mains = soup.find_all("section")

    nutrients = {}
    groups = list(*mains[0].find_all_next("h2", class_="pr__ind_head"))
    for t in groups:
        group = t.get_text("|", strip=True)
        ul = t.find_next_sibling("ul")
        for li in ul.find_all("li"):
            id_ = li.a["href"].split("/")[-1]

            # WTF?! https://fitaudit.ru/nutrients/fat_trans_polyenoic
            if id_ in NUTRIENTS_TO_SKIP:
                continue

            nutrient = {"group": group, "name": li.a.text, "id": id_}
            nutrients.update({id_: nutrient})
            await q.put(id_)

    return nutrients


async def scrape_nutrients(session: ClientSession, save: bool) -> int:
    """Scrape Nutrients Page."""
    to_rich_q = asyncio.Queue()
    rich_out_q = asyncio.Queue()

    soup = await get_soup_from_http(nutrients_path, nutrients_soup, session)
    nutrients = await eat(soup, to_rich_q)

    n = 50

    nutrient_getters = create_tasks(
        n, get_nutrient_richup_info, to_rich_q, rich_out_q, session
    )

    nutrient_updater = create_tasks(2, update_nutrient, rich_out_q, nutrients)

    await to_rich_q.join()
    cancel_tasks(nutrient_getters)

    await rich_out_q.join()
    cancel_tasks(nutrient_updater)

    if save:
        await save_json(nutrients_json, nutrients)

    return len(nutrients)
