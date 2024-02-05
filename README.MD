# Web Scraping
This project has been developed to learn the ETL process using the website "https://books.toscrape.com".

I've developed three scripts that scrape in the following order: one book, all books from a chosen category, and all books from all categories. These books are then saved into a CSV file.

# Prerequisites
Requests
BeautifulSoup
Urllib3

# Installation

## Clone the repository:
`
git clone https://github.com/PlantBasedStudio/WebScraping.git
`

## Navigate to the project directory:
`
cd WebScraping
`

## Create and activate a virtual environment (optional but recommended):
`
python3 -m venv venv
source venv/bin/activate
`

## Install the required dependencies using pip:
`
pip install -r requirements.txt
`

# Usage
scrap_a_book: Scrapes a single book and generates a CSV file (change the URL to use it).
scrap_a_category: Scrapes all books from a chosen category and generates a CSV file (change the URL to use it).
scrap_all_books_per_category: Scrapes all books from the website and generates a CSV file per category.

# Author
PlantBasedStudio : https://github.com/PlantBasedStudio