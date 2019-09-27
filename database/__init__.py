#!/usr/bin/python
import mysql.connector
from common.str2time import str2time
from article import Article
import common.consol_formating as console
from common.log_data import log_append_data_into_file


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="****",
    database='dbName'
)


def write_to_db(mydb, sql, val):
    my_cursor = mydb.cursor()
    # Writing in the Data Base
    my_cursor.execute(sql, val)
    mydb.commit()
    return


def read_form_db(mydb, sql):
    my_cursor = mydb.cursor()
    my_cursor.execute(sql)
    response = my_cursor.fetchall()
    return response


def check_article_exists(link):
    # Reading from Database
    sql = "SELECT url FROM article WHERE url = '" + link + "'"
    response = read_form_db(mydb, sql)
    if len(response) > 0:
        return True
    return False


def check_entity_exists(link):
    # Reading from Database
    sql = "SELECT url FROM entity WHERE url = '" + link + "'"
    response = read_form_db(mydb, sql)
    if len(response) > 0:
        return True
    return False


def check_source_exists(link):
    # Reading from Database
    sql = "SELECT url FROM sources WHERE url = '" + link + "'"
    response = read_form_db(mydb, sql)
    if len(response) > 0:
        return True
    return False


def is_connection_duplicate(article_id, entity_id):
    sql = "SELECT id FROM article2entity WHERE article_id = " + str(article_id) + " AND entity_id = " + str(entity_id)
    response = read_form_db(mydb, sql)
    if len(response) > 0:
        return True
    return False


def get_article_date(link):
    art = Article(link)
    para = art.paragraphs
    date = para.pop(0)
    a_date = ''

    if len(date) == 1:
        a_date = str2time(date[0])

    return a_date


def get_article_text(link):
    art = Article(link)
    para = art.paragraphs
    a_text = ''
    for l in para:
        print(l)
        for p in l:
            a_text = a_text + p

    return a_text


def get_article_id(link):
    sql_a = "SELECT id FROM article WHERE url = '" + link + "'"
    resp_a = read_form_db(mydb, sql_a)
    if len(resp_a) > 0:
        return resp_a[0][0]
    return 0


def get_entity_id(link):
    sql_e = "SELECT id FROM entity WHERE url = '" + link + "'"
    resp_e = read_form_db(mydb, sql_e)
    if len(resp_e) > 0:
        return resp_e[0][0]
    return 0


def get_source_id(link):
    sql_e = "SELECT id FROM sources WHERE url = '" + link + "'"
    resp_e = read_form_db(mydb, sql_e)
    if len(resp_e) > 0:
        return resp_e[0][0]
    return 0


def get_paragraph_id(article_id, paragraph_index):
    sql_p = "SELECT id FROM paragraph WHERE article_id = '" + str(article_id) + \
            "' AND paragraph_index = '" + str(paragraph_index) + "'"
    resp_p = read_form_db(mydb, sql_p)
    if len(resp_p) > 0:
        return resp_p[0][0]
    return 0


def write_new_entity(e_link, name):
    sql = "INSERT INTO entity (url, name) VALUES (%s, %s)"
    val = (e_link, name)
    write_to_db(mydb, sql, val)

    return


def write_new_artical2entity(original_string, artical_id, entity_id, start_index, end_index, pharagraph_id):
    sql = "INSERT INTO article2entity (article_id, entity_id, original_string, start_index, end_index, paragraph_id) " + \
          "VALUES (%s, %s, %s, %s, %s, %s)"
    val = (artical_id, entity_id, original_string, start_index, end_index, pharagraph_id)
    write_to_db(mydb, sql, val)

    return


def write_new_entities_and_connect_to_article(link):
    console.print_green('    -> Write New Entities in to DB')
    article_id = get_article_id(link)
    art = Article(link)
    entities = art.entities

    for epl, p_idx in zip(entities, range(len(entities))):
        for l1 in epl:
            for e in l1:
                print(e[0][0], e[1][0])
                entity_id = 0
                name_e = e[0][0]
                link_e = e[0][1]
                if not check_entity_exists(link_e):
                    write_new_entity(link_e, name_e)

                entity_id = get_entity_id(link_e)
                start_index = e[1][0]
                end_index = e[1][1]
                paragraph_id = e[1][2]
                write_new_artical2entity(name_e, article_id, entity_id, start_index, end_index, paragraph_id)


def write_new_paragraphs(link):
    art = Article(link)
    para = art.paragraphs
    a_id = get_article_id(link)

    if a_id != 0:
        for p, idx in zip(para, range(len(para))):
            sql = "INSERT INTO paragraph (article_id, text, paragraph_index) VALUES (%s, %s, %s)"
            val = (a_id, p[0], idx)
            write_to_db(mydb, sql, val)
            print(p)
    else:
        print('There is a problem the article is not into the DB !!!')


def write_new_article(link):
    # Writing in the Data Base
    art = Article(link)
    title = art.topic

    # a_date = get_article_date(link)
    a_text = get_article_text(link)

    # sql = "INSERT INTO article (url, title, publication_date, text) VALUES (%s, %s, %s, %s)"
    # val = (link, title, a_date, a_text)

    sql = "INSERT INTO article (url, title, text) VALUES (%s, %s, %s)"
    val = (link, title, a_text)

    write_to_db(mydb, sql, val)

    return


def write_new_source(link):

    try:
        art = Article(link)
        a_sources = art.sources

        for source in a_sources:
            if len(source) == 2:
                if not check_source_exists(source[0]):
                    # Write Source
                    sql = "INSERT INTO sources (url, date) VALUES (%s, %s)"
                    val = (source[0], source[1])
                    write_to_db(mydb, sql, val)

                # Write source-article connection
                a_id = get_article_id(link)
                s_id = get_source_id(source[0])
                sql = "INSERT INTO source2article (article_id, source_id) VALUES (%s, %s)"
                val = (a_id, s_id)
                write_to_db(mydb, sql, val)

                print(source[0])
    except:
        console.print_warning('Problem with source writing of the link: ' + link)
        log_append_data_into_file('log_sources.txt', 'Link Source Parsing Problem: ' + link + '\n')

    return
