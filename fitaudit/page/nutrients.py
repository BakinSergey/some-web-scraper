import asyncio
from asyncio import Queue

from aiohttp import ClientSession
from bs4 import BeautifulSoup as Soup

from fitaudit import products_json, products_path, CHUNK, products_soup, nutrients_path, nutrients_soup, nutrients_json, \
    NUTRIENTS_TO_SKIP
from fitaudit.detail.nutrient import get_nutrient_richup_info, update_nutrient
from fitaudit.detail.product import get_product_richup_info, update_products
from fitaudit.utils.a_json import save_chunked, save_json
from fitaudit.utils.soup import get_soup_from_http
from fitaudit.utils.tasks import create_tasks, cancel_tasks


async def eat(soup: Soup, q: Queue):
    mains = soup.find_all('section')

    nutrients = {}
    groups = [i for i in mains[0].find_all_next('h2', class_='pr__ind_head')]
    for t in groups:
        group = t.get_text("|", strip=True)
        ul = t.find_next_sibling('ul')
        for li in ul.find_all('li'):
            id_ = li.a['href'].split('/')[-1]

            # WTF?! https://fitaudit.ru/nutrients/fat_trans_polyenoic
            if id_ in NUTRIENTS_TO_SKIP:
                continue

            nutrient = {
                'group': group,
                'name': li.a.text,
                'id': id_
            }
            nutrients.update({id_: nutrient})
            await q.put(id_)

    return nutrients


async def scrape_nutrients(session: ClientSession, save: bool) -> int:
    to_rich_q = asyncio.Queue()
    rich_out_q = asyncio.Queue()

    soup = await get_soup_from_http(nutrients_path, nutrients_soup, session)
    nutrients = await eat(soup, to_rich_q)

    n = 50

    nutrient_getters = create_tasks(n, get_nutrient_richup_info,
                                    to_rich_q, rich_out_q, session)

    nutrient_updater = create_tasks(2, update_nutrient, rich_out_q, nutrients)

    await to_rich_q.join()
    cancel_tasks(nutrient_getters)

    await rich_out_q.join()
    cancel_tasks(nutrient_updater)

    if save:
        await save_json(nutrients_json, nutrients)

    return len(nutrients)
