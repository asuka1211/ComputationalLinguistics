from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from datetime import timedelta, datetime
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread
import json
from selenium.common.exceptions import WebDriverException as WDE
import requests
from bs4 import BeautifulSoup
import pymongo
import Tomita_parse
import datetime



chrome_options = webdriver.ChromeOptions()
client = pymongo.MongoClient(
    "mongodb+srv://Admin:12345@db1-9o4za.mongodb.net/db1?retryWrites=true&w=majority")
db = client.newsDB
news = []
news_link = 'https://www.volgograd.kp.ru/online/news/'
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--remote-debugging-port=9222')


driver = webdriver.Chrome(
    "/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)
driver.maximize_window()
driver.get('https://www.volgograd.kp.ru/online/')


def date_switch(arg):
    switcher = {
        "Январь": 1,
        "Февраль": 2,
        "Март": 3,
        "Апрель": 4,
        "Май": 5,
        "Июнь": 6,
        "Июль": 7,
        "Август": 8,
        "Сентябрь": 9,
        "Октябрь": 10,
        "Ноябрь": 11,
        "Декабрь": 12
    }

    datetime1 = arg
    arr = datetime1.split(" ")
    day = arr[0]
    year = arr[1][-4:]
    mounth = switcher.get(arr[1][:-4])
    day = str(day)
    mounth = str(mounth)
    year = str(year)

    date = year + ' ' + mounth + ' ' + day
    datt = datetime.datetime.strptime(date, "%Y %m %d")
    return datt

# Количество проходов по ленте
for x in range(2):

    time.sleep(2)
    driver.find_element_by_xpath(
        '/html/body/div[1]/main/div[1]/section/div[1]/div/div[3]/div[2]/div/article[1]/div[3]/span/a').send_keys(Keys.END)


a = driver.find_elements_by_id('newsRegionContentJS')
time.sleep(3)
for c in a:
    c = c.find_elements_by_tag_name('article')
for b in c:

    news.append({
        'Link': news_link + b.get_attribute('id')
    })
print(len(news))
print('Selenium:Done')
news_discription = ''
title = []
URL = []
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 'Accept': '*/*'}

http = 'http:'

for g in news:
    URL = g['Link']

    def get_html(url, params=None):
        r = requests.get(url, headers=HEADERS, params=params)
        return r

    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')

        img = soup.find("img", {"class": "image"}).get(
            'src') if soup.find("img", {"class": "image"}) else ''

        news_discription = soup.find(
            "div", {"class": "text js-mediator-article"}).get_text()

        # from_db = db.news.find({}, {"_id": 0, "title": 1})
        now = soup.find("time").get_text()
        datett = date_switch(now)
        name = soup.find("h1").get_text()
        cursor = len(list(db.news.find({'title': name})))
        if cursor:
            return
        Tomita_parse.start(news_discription)
        

        db.news.insert_one({
            'title': soup.find("h1").get_text(),
            'link': URL,
            'discription': soup.find("div", {"class": "text js-mediator-article"}).get_text(),
            'img': http + img,
            'date': datett

        })

    def parce():
        html = get_html(URL)
        if html.status_code == 200:

            parce_result = get_content(html.text)

        else:
            print('Что то пошло не так')
        return(parce_result)

    result = parce()


print('Done')
