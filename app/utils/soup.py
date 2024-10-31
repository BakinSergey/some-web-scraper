"""Create Soup fns."""

import asyncio
from typing import Optional

import aiofiles
from aiohttp import ClientSession as Session
from bs4 import BeautifulSoup as Soup

from app import SAVE_DETAIL_SOUP, SAVE_SOUP, SOURCE, pages


async def get_soup_from_http(url, soup_name, session: Session) -> Optional[Soup]:
    """Get Soup object from downloaded HTML."""
    r = await session.get(url)
    if r.ok:
        html_src = await r.text()
        soup = await asyncio.to_thread(Soup, html_src, "lxml")

        is_page = soup_name in pages

        if SAVE_SOUP and is_page:
            async with aiofiles.open(SOURCE / soup_name, mode="w") as f:
                await f.write(html_src)

        if SAVE_DETAIL_SOUP:
            async with aiofiles.open(SOURCE / soup_name, mode="w") as f:
                await f.write(html_src)

        return soup
    else:
        print(f"{r.status}: {await r.text()}")


async def get_soup_from_html(file: str) -> Soup:
    """Get Soup object from HTML file."""
    async with aiofiles.open(SOURCE / file, mode="r") as f:
        html_src = await f.read()

    return Soup(html_src, "lxml")
