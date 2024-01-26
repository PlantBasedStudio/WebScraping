import re
import csv
import requests
from bs4 import BeautifulSoup
from datetime import date
from urllib.parse import urljoin


def scrap(url_link):
    response = requests.get(url_link)
    if not response.ok:
        return print("Error : Wrong URL")
    else:
        soup_response = BeautifulSoup(response.text, 'html.parser')
        return soup_response


url = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"


books = []


def extract_book_data(soup, url):
    print("Scrap d'un livre")
    items = {}
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
    print("Scrap de " + book_data_dict['title'] + " terminé.")
    books.append(book_data_dict)


soup_page = scrap(url)

books_links = []


def transform_url(base_url, relative_url):
    parts = relative_url.split('/')
    book_name = parts[3]
    final_url = urljoin(base_url, f'/catalogue/{book_name}/index.html')
    return final_url


def scrap_links_in_page(url_link):
    soup = scrap(url_link)
    articles = soup.find_all('article', class_='product_pod')
    for article in articles:
        title_link = article.find('h3')
        link = title_link.find('a').get('href')
        complete_link = transform_url(url_link, link)
        books_links.append(complete_link)


scrap_links_in_page(url)


new_extend_link = 'index.html'
new_link = url
#
#
def detect_pages(new_link):
    print("Detection des pages")
    soup = scrap(new_link)
    if soup.find_all('ul', class_="pager"):
        if soup.find('li', class_="next"):
            print("Nouvelle page trouvée")
            return True
        else:
            print("Pas d'autre page")
            return False
    else:
        print("Pas d'autre page")
        return False


while detect_pages(new_link):
    soup = scrap(new_link)
    print("On cherche le lien")
    li = soup.find('li', class_="next")
    print("Le lien est bon")
    a = li.find('a').get('href')
    print("Lien :" + str(a))
    print("extension :" + new_extend_link)
    new_link = new_link.replace(new_extend_link, a)
    new_extend_link = a
    print("Nouvelle extension de lien : " + new_extend_link)
    print("Nouveau lien : "  + new_link)
    scrap_links_in_page(new_link)

for book in books_links:
    extract_book_data(scrap(book), book)

# CSV part
print("Génération d'un fichier excel")
header = books[0].keys()
today = str(date.today())

with open(books[0]['category'].replace(" ", "_") + "_" + today + "_data.csv", "w", newline='', encoding='utf-8') as file_csv:
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(header)
    for book in books:
        line = book.values()
        writer.writerow(line)

    print("Votre fichier Excel est prêt")