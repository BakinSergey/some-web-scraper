import asyncio
from asyncio import create_task
import time
from pprint import pprint

import aiohttp

from fitaudit import SAVE
from fitaudit.page.categories import scrape_categories
from fitaudit.page.products import scrape_products
from fitaudit.page.nutrients import scrape_nutrients


async def main():
    async with aiohttp.ClientSession() as session:
        categories = create_task(scrape_categories(session, SAVE))
        producties = create_task(scrape_products(session, SAVE))
        nutrientos = create_task(scrape_nutrients(session, SAVE))

        await asyncio.gather(*[producties, categories, nutrientos])

        scraped = {
            'categories': categories.result(),
            'nutrients': nutrientos.result(),
            'products': producties.result(),
            # scrape_norm()
        }

        pprint(scraped)


if __name__ == "__main__":
    start = time.time()

    asyncio.run(main())

    print(time.time() - start)
