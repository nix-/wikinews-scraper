import main_page_news as main_page
from article import Article

# Getting the articles from the main page (the ones in focus)
for article in main_page.get_main_news_links():
    link_to_article = article[0] # http link to the article
    a = Article(link_to_article)
    a.print()
    print(a.get_content())

# Getting the articles from the side panel latest-news (the one on the right side)
for article in main_page.get_latest_news_links():
    link_to_article = article[0] # http link to the article
    a = Article(link_to_article)
    a.print()
    print(a.get_content())
