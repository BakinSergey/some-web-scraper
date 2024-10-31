"""common project data."""

from pathlib import Path

CHUNK = 1024
SAVE = True
SAVE_SOUP = True
SAVE_DETAIL_SOUP = False

NUTRIENTS_TO_SKIP = ["fat_trans_polyenoic"]

# fmt: off
PROJECT = Path(__file__).parent
SOURCE = PROJECT / 'in'
TARGET = PROJECT / 'out' / 'scraped'

SOURCE.mkdir(parents=True, exist_ok=True)
TARGET.mkdir(parents=True, exist_ok=True)

# categories
categories_path = 'https://fitaudit.ru/categories'
categories_soup = 'soup_categories.html'
categories_json = 'categories.json'

# nutrients
nutrients_path = 'https://fitaudit.ru/nutrients'
nutrients_soup = 'soup_nutrients.html'
nutrients_json = 'nutrients.json'

# products
products_path = 'https://fitaudit.ru/food'
products_soup = 'soup_products.html'
products_json = 'products.json'

# detail views
nutrient_path = 'https://fitaudit.ru/nutrients/{}'
nutrient_soup = 'nutrient_soup_{}.html'

product_path = 'https://fitaudit.ru/food/{}'
product_soup = 'product_soup_{}.html'

# fmt: on

pages = [categories_soup, products_soup, nutrients_soup]
