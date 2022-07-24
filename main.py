import csv
import datetime
import requests
from bs4 import BeautifulSoup as BS

URL = f"https://habr.com/ru/all/page"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                         '(KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', 'accept': '*/*'}

#Поиск по словам в тексте
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
HOST = "https://habr.com"


def log_decor_for_path():
    def log_decor(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            logger = (f'Функция  {old_function.__name__} запущена {datetime.datetime.now()}, '
                      f'результат: {result}')

            with open('loger.txt', "w") as file:
                file.write(logger)

            return result

        return new_function

    return log_decor


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_content(html):
    soup = BS(html, 'html.parser')
    items = soup.find_all('article', class_='tm-articles-list__item')
    data_list = []
    for item in items:
        for keyword in KEYWORDS:
            if keyword in item.get_text():
                datearticle = item.find('span', class_="tm-article-snippet__datetime-published").get_text()
                titlearticle = item.find('h2',
                                         class_="tm-article-snippet__title tm-article-snippet__title_h2").get_text()
                link = HOST + item.find('a', class_="tm-article-snippet__title-link").get('href')
                data = datearticle, titlearticle, link
                data_list.append(data)
    return data_list


@log_decor_for_path()
def parse(count_page=3):
    for count in range(count_page):
        html = get_html(URL+str(count+1))
        if html.status_code == 200:
            print(get_content(html.text))
        else:
            print("Error")
    return 'Success'

parse()
