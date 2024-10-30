from fitaudit.detail.nutrient_parser import nutrient_info_parser

import asyncio
from queue import Queue

from fitaudit import nutrient_path, nutrient_soup
from fitaudit.utils.soup import get_soup_from_http


async def update_nutrient(q: Queue, nutrients: dict[str, dict]) -> None:
    while True:
        (id_, rich_info) = await q.get()
        nutrients.get(id_).update(rich_info)
        q.task_done()
        print(id_)


async def get_nutrient_richup_info(in_q, out_q, session) -> None:
    while True:
        id_ = await in_q.get()
        soup_url = nutrient_path.format(id_)
        soup_name = nutrient_soup.format(id_)

        soup = await get_soup_from_http(soup_url, soup_name, session)

        rich_info = await asyncio.to_thread(nutrient_info_parser, soup)
        await out_q.put((id_, rich_info))

        in_q.task_done()
