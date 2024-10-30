import asyncio

from aiohttp import ClientSession
from bs4 import Tag
from bs4 import BeautifulSoup as Soup

from fitaudit import categories_soup, categories_path, categories_json, CHUNK
from fitaudit.utils.a_json import save_chunked
from fitaudit.utils.soup import get_soup_from_http


class Types:
    INT = int
    STR = str
    TAG = Tag


def get_category(t: Tag) -> dict:
    ttl = t.a.text.strip()
    ico = t.a.span.attrs['class'][-1]
    return {'category':
                {'ico': ico,
                 'ttl': ttl}
            }


def eat(soup: Soup):
    main_cls = 'flist__li_main'
    sub_cls = 'flist__li_sub'

    mains = soup.find_all('li', class_=main_cls)

    categories = list()

    for mn in mains:
        sub_categories = []
        for sb in mn.next_siblings:
            match type(sb):
                case Types.STR:
                    continue
                case Types.TAG:
                    if main_cls in sb['class']:
                        break
                    elif sub_cls in sb['class']:
                        sub_categories.append(get_category(sb))

        category = get_category(mn)
        if sub_categories:
            category['category'].update({'subcategories': sub_categories})

        categories.append(category)

    return categories


async def scrape_categories(session: ClientSession, save: bool):
    soup = await get_soup_from_http(categories_path, categories_soup, session)
    categories = await asyncio.to_thread(eat, soup)

    if save:
        await save_chunked(categories_json, categories, CHUNK)
    return len(categories)
