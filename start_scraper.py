#!/usr/bin/python

import common.consol_formating as console

from main_page_news import get_latest_news_links
from main_page_news import get_main_news_links

from article import Article
import database as db


def processed_related_articles(link_r, deepness):
    if deepness == 0:
        console.print_green('>> Recursion LOWEST Level is Reached << ')
        return 0
    else:
        art = Article(link_r)
        rel_links = art.related
        for rel in rel_links:

            if len(rel) > 0:
                lin = rel[0]

                if not db.check_article_exists(lin):
                    console.print_green('>> Recursion LEVEL: ' + str(deepness) + console.CS.ENDC +
                                        '   (new article)' +
                                        '\r\n\t\t' + lin)
                    db.write_new_article(lin)
                    db.write_new_source(lin)
                    db.write_new_paragraphs(lin)
                    db.write_new_entities_and_connect_to_article(lin)
                    # Recursive call
                    processed_related_articles(lin, deepness - 1)
                else:
                    console.print_blue('>> Recursion LEVEL: ' + str(deepness) + console.CS.ENDC +
                                        '\t' + lin)

        return deepness


deepness_level = 100  # defining the deepness of diving


def dive(deepnees):

    news_list = get_main_news_links() + get_latest_news_links()

    for item in news_list:

        link = item[0]

        # Check the articles from the main page
        if not db.check_article_exists(link):
            console.print_green('>> Recursion LEVEL: root' + console.CS.ENDC +
                                '   (new article)' +
                                '\r\n\t\t' + link)
            db.write_new_article(link)
            db.write_new_source(link)
            db.write_new_paragraphs(link)
            db.write_new_entities_and_connect_to_article(link)
            processed_related_articles(link, deepnees)

        else:
            console.print_blue('>> Recursion LEVEL: root' + console.CS.ENDC +
                                '\t' + link)

        return


dive(deepness_level)
