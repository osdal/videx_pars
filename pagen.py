# import videx_categoriex
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

url = 'https://videx.ua/'
response = requests.get(url=url, headers=headers)
html = response.text
soup = bs(html, 'html.parser')

dom = etree.HTML(str(soup))


def get_categoty_up_link(dom):
    category_up_link = dom.xpath("//header//div[@class='categories']/div/ul/li/"
                                 "a[not(@rel = 'nofollow')]")
    for link in category_up_link:
        category_up_links = [url + link.get('href') for link in category_up_link]
    return category_up_links


def get_number_pages(dom_category):
    number_pages_block = dom_category.xpath("//ul[contains(@class, 'pagination')]//"
                                            "li[not(descendant::span)]/a/text()")
    num_pages = number_pages_block[-1]
    print('Categoty ' + url_category + ' include ' + num_pages)
    number_pages.append(num_pages)
    return number_pages


number_pages = []
url_categories = get_categoty_up_link(dom)
for url_category in url_categories:
    response = requests.get(url=url_category, headers=headers)
    html = response.text
    soup_category = bs(html, 'html.parser')

    dom_category = etree.HTML(str(soup_category))
    number_pages = get_number_pages(dom_category)


def get_page_link(url_category, number_page):
    page_link = url_category + f'/page-{number_page}'
    return page_link


cat_link_num = [{'link': link, 'number': number} for link, number in zip(url_categories, number_pages)]

link_page_list = []
for i in range(0, len(cat_link_num)):
    link_page_root = cat_link_num[i]['link']
    for n in range(1, int(cat_link_num[i]['number']) + 1):
        link_page = link_page_root + f'/page-{n}'
        link_page_list.append(link_page)
print(link_page_list)



# Ваш список данных
# data = [
#     ['Имя', 'Возраст', 'Город'],
#     ['Анна', 25, 'Москва'],
#     ['Петр', 30, 'Санкт-Петербург'],
#     ['Елена', 35, 'Новосибирск']
# ]
link_page_list
# Укажите путь к файлу CSV
csv_file_path = './DATA/link_page_list.csv'

# Записываем данные в файл CSV
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    for item in link_page_list:
        writer.writerow([item])

print("Данные сохранены в файл CSV.")
