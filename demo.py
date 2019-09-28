from article import Article
import main_page_news as main_page
from console import CS

# The code is colecting all of the links from the main wikinews page
# and colecting information from the articles

# Getting the articles from the main page (the ones in focus)
for article in main_page.get_main_news_links():

    article_link = article[0] # http link to the article

    # the constructor is colecting all of the article data
    a = Article(article_link)
    a.print() # general info-print

    # accessing information from the article
    CS.print_blue('\n ### Acesses example ->')
    print(a.get_heading())
    print(a.get_paragraph())
    print(a.get_entities())

# Getting the articles from the side panel latest-news (the one on the right side)
for article in main_page.get_latest_news_links():

    article_link = article[0] # http link to the article

    # the constructor is colecting all of the article data
    a = Article(article_link)

    # accessing information from the article
    CS.print_green('\n ### Acesses example ->')
    print(a.get_content())
    print(a.get_entities())
    print(a.get_related())
