import re
import csv
import requests
from bs4 import BeautifulSoup


def scrap(url_link):
    response = requests.get(url_link)
    if not response.ok:
        return print("Error : Wrong URL")
    else:
        soup_response = BeautifulSoup(response.text, 'html.parser')
        return soup_response


url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

items = {}


def extract_book_data(soup):
    trs = soup.find_all('tr')
    for tr in trs:
        th = tr.find('th')
        item_name = th.string
        td = tr.find('td')
        item_value = td.string
        items[item_name] = item_value
    product_page_url = url
    universal_product_code = items['UPC']
    title = soup.find('h1').string
    price_including_tax = items['Price (incl. tax)']
    price_excluding_tax = items['Price (excl. tax)']
    number_available = items['Availability']
    product_description_div = soup.find('div', id="product_description")
    product_description = product_description_div.find_next_sibling('p').string
    category_list = soup.find('ul', class_='breadcrumb')
    category = category_list.find_all('a')[-1].string
    rate = soup.find('p', class_=re.compile(r'star-rating'))
    rate_classes = rate.get('class')
    review_rating = rate_classes[-1]
    image_url = soup.find('img').get('src')
    book_data_dict = {
        'product_page_url': product_page_url,
        'universal_product_code': universal_product_code,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'review_rating': review_rating,
        'image_url': image_url
    }

    return book_data_dict


soup_data = scrap(url)
book_data = extract_book_data(soup_data)


# CSV part
header = []
for key in book_data:
    header.append(key)

with open("data.csv", "w") as file_csv:
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(header)
    line = []
    for value in book_data.values():
        line.append(value)
    writer.writerow(line)# writer.writerow(line)