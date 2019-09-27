from article import Article
from bs4 import BeautifulSoup
import requests
import database as db
import datetime
from start_scraper import processed_related_articles



link = 'https://en.wikinews.org/wiki/Toronto%27s_Anime_North_2019_brings_thousands_of_fans_together'
#link = 'https://en.wikinews.org/wiki/FIFA_World_Cup_2018_day_eight,_nine,_ten,_eleven:_Belgium,_England_confirm_knockout_phase_qualification;_Poland,_Costa_Rica_miss_out_Last_16'
#link = 'https://foundation.wikimedia.org/wiki/Privacy_policy'

a1 = Article(link)
a1.print()

if db.check_article_exists(link):
    print('Old article')
else:
    print('New article')

now = datetime.datetime.now()
print(now.year, now.month, now.day, now.hour, now.minute, now.second)

years = range(2005, int(now.year+1))

for year in years:
    link = 'https://en.wikinews.org/wiki/Wikinews:'+str(year)
    soup = BeautifulSoup(requests.get(link).content, 'html.parser').\
        find('div', attrs={"class": "mw-parser-output"})
    if soup:
        m_list = soup.find_all('a')
        if m_list:
            for m in m_list:
                y_link = 'https://en.wikinews.org' + m['href']
                y_soup = BeautifulSoup(requests.get(y_link).content, 'html.parser')\
                    .find_all('ul')
                for e in y_soup:
                    l = e.find_all('a')
                    if l:
                        if l[0]['href'].startswith('/wiki/'):
                            lnk = 'https://en.wikinews.org' + l[0]['href']
                            try:
                                if not db.check_article_exists(lnk):
                                    db.write_new_article(lnk)
                                    db.write_new_source(lnk)
                                    db.write_new_paragraphs(lnk)
                                    db.write_new_entities_and_connect_to_article(lnk)
                            except:
                                print('except: ' + lnk)

