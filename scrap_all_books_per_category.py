import re
import csv
import requests
import os
from bs4 import BeautifulSoup
from datetime import date
from urllib.parse import urljoin
import urllib.request


def scrap(url_link):
    response = requests.get(url_link)
    if not response.ok:
        return print("Error : Wrong URL")
    else:
        soup_response = BeautifulSoup(response.text.encode('utf-8'), 'html.parser')
        return soup_response


url = "https://books.toscrape.com/index.html"
base_url = "https://books.toscrape.com/"

cat_links = []
cat_books = []
books = []


def transform_url(base_url, relative_url):
    parts = relative_url.split('/')
    book_name = parts[3]
    final_url = urljoin(base_url, f'/catalogue/{book_name}/index.html')
    return final_url


def transform_image_url(base_url, relative_url):
    parts = relative_url.split('/')
    book_name = parts[3]
    final_url = urljoin(base_url, relative_url)
    return final_url


def download_images(book_data):
    for book in book_data:
        category = book['category']
        image_url = transform_image_url('https://books.toscrape.com', book['image_url'])
        image_name = re.sub(r'[^\w\s]', '_', book['title'])
        category_folder = os.path.join("Images", category)

        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        if not image_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_name += '.jpg'

        image_path = os.path.join(category_folder, image_name)

        try:
            print(image_url)
            urllib.request.urlretrieve(image_url, image_path)
            print(f"Image téléchargée : {image_name}")
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image {image_name}: {e}")


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
    if soup.find('div', id="product_description"):
        product_description_div = soup.find('div', id="product_description")
        product_description = product_description_div.find_next_sibling('p').string
    else:
        product_description = ""
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
        'image_url': image_url,
    }
    print("Scrap de " + book_data_dict['title'] + " terminé.")
    books.append(book_data_dict)
    return book_data_dict


def scrap_links_in_page(url_link):
    soup = scrap(url_link)
    articles = soup.find_all('article', class_='product_pod')
    for article in articles:
        title_link = article.find('h3')
        link = title_link.find('a').get('href')
        complete_link = transform_url(url_link, link)
        books_links.append(complete_link)


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


def scrap_all_category(url_link):
    soup = scrap(url_link)
    div = soup.find('div', class_='side_categories')
    li = div.find('li')
    ul = li.find('ul')
    link = ul.find_all('a')
    for href in link:
        complete_link = (base_url + href.get('href'))
        cat_links.append(complete_link)


scrap_all_category(url)


for cat in cat_links:
    books_links = []
    all_books_in_this_cat = []
    new_link = cat
    new_extend_link = 'index.html'
    scrap_links_in_page(new_link)
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
        print("Nouveau lien : " + new_link)
        scrap_links_in_page(new_link)
    all_books_in_this_cat.append(books_links)
    cat_books.append(all_books_in_this_cat)


# CSV part
today = str(date.today())

for categories in cat_books:
    print("Génération d'un fichier excel")

    for book_group in categories:
        with open("Category_" + extract_book_data(scrap(book_group[0]), book_group)['category'] + today + "_data.csv", "w",
                  newline='', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv, delimiter=",")
            header = extract_book_data(scrap(book_group[0]), book_group).keys()
            writer.writerow(header)
            for book in book_group:
                line = extract_book_data(scrap(book), book).values()
                writer.writerow(line)
    print("Votre fichier Excel est prêt")

download_images(books)
