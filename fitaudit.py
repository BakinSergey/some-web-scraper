"""Project for training AsyncIO, HTML-Scrape technics."""

import asyncio
import time
from asyncio import create_task
from pprint import pprint

import aiohttp

from app import SAVE
from app.page.categories import scrape_categories
from app.page.nutrients import scrape_nutrients
from app.page.products import scrape_products


async def main():
    """Scrape: Categories, Products, Nutrients."""
    async with aiohttp.ClientSession() as session:
        categories = create_task(scrape_categories(session, SAVE))
        producties = create_task(scrape_products(session, SAVE))
        nutrientos = create_task(scrape_nutrients(session, SAVE))

        await asyncio.gather(*[producties, categories, nutrientos])

        scraped = {
            "categories": categories.result(),
            "nutrients": nutrientos.result(),
            "products": producties.result(),
            # scrape_norm()
        }

        pprint(scraped)


if __name__ == "__main__":
    start = time.time()

    asyncio.run(main())

    print(time.time() - start)
