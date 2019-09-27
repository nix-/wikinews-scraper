#!/usr/bin/python
import requests
from bs4 import BeautifulSoup


def get_latest_news_links():
    # Collect Articles of Focus
    resp = requests.get("https://en.wikinews.org/wiki/Main_Page");
    soup = BeautifulSoup(resp.content, 'html.parser');

    # Collect Articles from Latest News
    latest_news = soup.find('div', attrs={"id": "MainPage_latest_news_text"}).find_all('a')
    l_list = [['https://en.wikinews.org' + x['href'], x.text] for x in latest_news]

    return l_list


def get_main_news_links():
    # Collect Articles of Focus
    resp = requests.get("https://en.wikinews.org/wiki/Main_Page");
    soup = BeautifulSoup(resp.content, 'html.parser');

    articles = soup.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['l_box'])

    m_list = [['https://en.wikinews.org' + x.find('a')['href'],
               x.find('span', attrs={"class": "l_title"}).find('a').text] for x in articles]

    return m_list


print(get_main_news_links())
print(get_latest_news_links())
