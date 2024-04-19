import csv
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree

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

url = page_links[0]
print(url)
response = requests.get(url, headers=headers)