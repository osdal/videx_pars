import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import re
import pandas as pd

books = []


def book_data(item):
    product = item.find('article', class_='product_pod')
    link = url + product.find('a').get('href')
    image = url + product.find('img').get('src')
    title = product.find('h3').find('a').get('title')
    price = product.find('p', class_='price_color').text
    book = {
        'title': title,
        'image': image,
        'price': price,
        'link': link
    }
    books.append(book)


url = "https://books.toscrape.com/"

# Get HTML
get_html = requests.get(url)

html = get_html.content

soup = bs(html, "html.parser")

list_category = (soup.find('div', class_='side_categories').
                 find('ul', class_='nav-list')).find('li').find('ul').findAll('li')

categories_href = []
categories_name = []
for category in list_category:
    category_href = url + category.find('a').get('href')
    categories_href.append(category_href)
    category_name = category.find('a').get_text(strip=True)
    categories_name.append(category_name)

for category_href in categories_href:
    response = requests.get(category_href)
    response_html = response.content
    soup = bs(response_html, "html.parser")
    book_data(soup)
print(books)
# Создаем общий список, каждый элемент которого - словарь
result = [{key: value} for key, value in zip(categories_name, categories_href)]

data = []
for p in range(1, 5):
    print(p)
    url_page = f'https://books.toscrape.com/catalogue/page-{p}.html'
    get_html = requests.get(url_page)
    # sleep(3)
    html = get_html.content
    soup = bs(html, "html.parser")

    books = soup.findAll('article', class_='product_pod')
    for book in books:
        link = 'https://books.toscrape.com/catalogue/' + book.find('a').get('href')
        title = book.find('h3').find('a').get('title')
        image = re.sub(r'\.\.', '', url + book.find('img').get('src'))
        price = book.find('p', class_='price_color').text
        data.append([link, title, image, price])

header = ['Link', 'Title', 'Image', 'Price']
df = pd.DataFrame(data, columns=header)
df.to_csv('./DATA/books.csv')
print(data)