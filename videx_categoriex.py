import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import csv
import pandas as pd
import os
import urllib.request
from urllib3.filepost import writer

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

response = requests.get("https://videx.ua/", headers=headers)
# print(html.status_code)
html = response.text
soup = bs(html, "html.parser")

dom = etree.HTML(str(soup))

def get_category_up_level():
    categories_up_level = dom.xpath("//header//li[@class='category_item has_child']/a/span")
    cat_up_level = []
    for category in categories_up_level:
        category = category.text
        cat_up_level.append(category)
    return cat_up_level

sub_categories = dom.xpath(f"//header//div[@class='categories']//"
                           f"ul[contains(@class, 'level_2')]")
sub_cat = []
for sub_category in sub_categories:
    sub_category = sub_category.xpath(".//li[@class='categories_menu__item']/a/span/text()")
    sub_cat.append(sub_category)
# print(len(sub_cat))
category_name = dom.xpath("//header//div[@class='categories']//a/span/text()")
# for name in category_name:
#     print(name)
# print(category_name)

links = []
category_link = dom.xpath("//header//div[@class='categories']//a")
for category in category_link:
    link = 'https://videx.ua/' + category.attrib['href']
    links.append(link)
# print(links)

images = []
category_img = dom.xpath("//header//div[@class='categories']//a/div/img")
for img in category_img:
    link_img = img.attrib['data-src']
    images.append(link_img)
    # print(link_img)
# print(images)
# category = [{key: value} for key, value in zip(cat_up_level, sub_cat)]

def get_categories():
    categories = []
    for i in range(len(category_name)):
        category = {
            'name': category_name[i],
            'link': links[i],
            'image': images[i]
        }
        categories.append(category)
    # print(categories)
    # for i in range(len(cat_up_level)):
    #     item = {
    #         cat_up_level[i]: sub_cat[i]
    #     }
    #     category.update(item)
    # print(category)
    return categories

# headers = cat_up_level
df = pd.DataFrame(get_categories())
df.to_csv('category.csv')


def download_img(url):
    subdirectory = 'PIC'
    # Создание директории
    os.makedirs(subdirectory, exist_ok=True)
    filepath = os.path.join(subdirectory, url.split("/")[-1])

    try:
        response = requests.get(url)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return 'Img successfully downloaded'

    except Exception as ex:
        return 'Img not downloaded'


for image in images:
    download_img(image)

# def main():
#     print(download_img(url=url1))
#
# if __name__ == '__main__':
#     main()

# urls = images
# directory = '/videx/PIC/'
# # Скачиваем изображения
# for url in urls:
#     response = requests.get(url)
#     filename = url.split("/")[-1]
#     with open(os.path.join(directory, filename), "wb") as f:
#         f.write(response.content)


# name_1 = 'Vasa'
# name_2 = 'Peta'
# names = ['Vita', 'Peta', 'Vasa', 'Peta', '']

# with open('data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(
#         # names
#
#     )

users = [
    ('name', 'category', 'sub_category'),
    ['Lamp', 'Svitlo', 'Electro'],
    ['Fonar', 'Svitlo', 'Podsvet'],
    ['Luke', 'Ender', 'Triolan']
]
# for user in users:
#     with open('data.csv', 'a') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(
#             user
#         )
# with open('data.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(users)

# Открываем файл CSV для записи с указанием кодировки UTF-8
# with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     # Создаем объект для записи CSV
#     writer = csv.writer(csvfile)
#
#     # Записываем заголовки
#     writer.writerow(category.keys())
#
#     # Получаем максимальную длину списка значений
#     max_length = max(len(value) for value in category.values())
#
#     # Записываем данные
#     # for i in range(max_length):
#     #     row = [category[key][i] if i < len(category[key]) else '' for key in category.keys()]
#     #     writer.writerow(row)
