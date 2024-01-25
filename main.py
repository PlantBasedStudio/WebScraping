import re

import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'


items = {}


def scrap(url_link):
    response = requests.get(url_link)
    if not response.ok:
        return print("Error : Wrong URL")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup



trs = scrap(url).find_all('tr')
for tr in trs:
    th = tr.find('th')
    item_name = th.string
    td = tr.find('td')
    item_value = td.string
    items[item_name] = item_value
print(items)

product_page_url = url
universal_product_code = items['UPC']
title = scrap(url).find('h1').string
price_including_tax = items['Price (incl. tax)']
price_excluding_tax = items['Price (excl. tax)']
number_available = items['Availability']
product_description_div = scrap(url).find('div', id="product_description")
product_description = product_description_div.find_next_sibling('p').string
category_list = scrap(url).find('ul', class_='breadcrumb')
category = category_list.find_all('a')[-1].string
rate = scrap(url).find('p', class_=re.compile(r'star-rating'))
rate_classes = rate.get('class')
review_rating = rate_classes[-1]
image_url = scrap(url).find('img').get('src')