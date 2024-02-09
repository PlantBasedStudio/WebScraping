import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def transform_stock(text):
    """
    Send a text to define is there is a number into it and return only the number
    :send_stock_data:
    :return number available or 0:
    """
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    else:
        return 0


def scrap(url_link):
    """
        Send a URL to scrap it and return pages
        :send_url:
        """
    response = requests.get(url_link)
    if not response.ok:
        return print("Error : Wrong URL")
    else:
        soup_response = BeautifulSoup(response.text.encode('UTF-8'), 'html.parser')
        return soup_response


def transform_url(base_url, relative_url):
    """
        Transform a URL for a book page
        :send_prefix_url:
        :send url to change:
        """
    parts = relative_url.split('/')
    book_name = parts[3]
    final_url = urljoin(base_url, f'/catalogue/{book_name}/index.html')
    return final_url


def detect_pages(new_link):
    """
        Detect if they are pages in this link
        :send_url:
        """
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