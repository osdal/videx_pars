import csv
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import time
import random

csv_file_path = './DATA/link_page_list.csv'

# Открываем файл CSV для чтения
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    # Создаем объект чтения CSV
    csv_reader = csv.reader(file)

    page_links = []

    # Проходимся по каждой строке в файле CSV и выводим ее
    for row in csv_reader:
        page_links.append(str(row[0]))
# print(page_links)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

for link in page_links:
    url = link
    response = requests.get(url, headers=headers)
    html = response.text
    soup = bs(html, 'html.parser')

    dom = etree.HTML(str(soup))

    product_links = dom.xpath("//div[@class='products_container']//a[@class='preview_image']/@href")

    prod_links = ['https://videx.ua/' + link for link in product_links]

    csv_file_path = './DATA/products_link.csv'
    # Записываем данные в файл CSV
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for item in prod_links:
            writer.writerow([item])
            # Выбираем случайное число из диапазона от 5 до 20
            delay = random.randint(5, 20)

            # Создаем задержку
            print(f"Задержка: {delay} секунд")
            time.sleep(delay)

print(len(prod_links))
