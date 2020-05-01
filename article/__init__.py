#!/usr/bin/python
import requests
import re
from bs4 import BeautifulSoup
from common.link_correction import correct_entity_link
from common.str2time import str2time
from console import CS as cs


class Article:
    def __init__(self, link=''):
        self.topic = ''
        self.date = ''
        self.paragraphs = ''
        self.content = ''
        self.img = ''
        self.soup = BeautifulSoup(requests.get(link).content, 'html.parser')

        if link == '':
            self.link = link
            self.entities = [[]]
            self.related = [[]]
            self.sources = [[]]

        else:  # the link is provided
            self.link = link
            self.topic = self.get_heading()
            self.paragraphs = self.get_paragraph()
            self.img = self.get_images()
            self.entities = self.get_entities()
            self.related = self.get_related_articles()
            self.sources = self.get_sources()

    def get_related(self):
        print('use link attribute ' + self.link)

    def get_sources(self):
        print('use link attribute ' + self.link)

    def get_heading(self):
        a_heading = self.soup.find('h1', attrs={"id": "firstHeading"})
        return a_heading.text

    def get_paragraph(self):
        a_paragraph = self.soup.find('div', attrs={"class": "mw-parser-output"}).find_all('p')
        list = [[p.text] for p in a_paragraph]
        return list

    def get_content(self):
        return ''.join([str(p[0]) for p in self.paragraphs])

    def get_images(self):
        # take the images from the article
        a_img = self.soup.find_all('div', attrs={"class": "thumbinner"})
        # todo: this need to be checked
        list = [[img_link_correction(x['src']) for x in imgs.find_all('img', attrs={"class": "thumbimage"})] for imgs in
                a_img]
        return list

    def get_entities(self):
        [s.extract() for s in self.soup('tbody')]  # remove tag 'tbody' all tables
        a_paragraph = self.soup.find('div', attrs={"class": "mw-parser-output"}).find_all('p')
        # Get Entities
        entities_in_paragraph = [[[e.text, e['href']] for e in n] for n in [m.find_all('a') for m in a_paragraph]]
        matching = [[[[correct_entity_link(entity), (match.start(), match.end(), idx)]
                      for match in re.finditer(entity[0], paragraph[0])]
                     for entity in entities]
                    for entities, paragraph, idx in zip(entities_in_paragraph, self.paragraphs,
                                                        range(len(self.paragraphs)))]
        return matching  # entities_in_paragraph

    def get_related_articles(self):
        [s.extract() for s in self.soup('tbody')]  # remove tag 'tbody' all tables
        # get related
        test_related = self.soup.find('div', attrs={"class": "infobox"})
        if test_related:
            a_related = test_related.find("ul").find_all('li')
            return [[("https://en.wikinews.org" + m.find('a')['href']), (m.find('a')['title'])] for m in a_related]
        return [[]]

    def get_sources(self):
        # Get the Sources from the Article
        sources = self.soup.find(text="Sources")
        if sources:
            sources = sources.findNext('ul').find_all('li')  # .contents[0]
            list = [[found_link(m.find('a', attrs={"class": "external text"})),
                     get_str_date(m.find_all(text=True, recursive=False))]
                    for m in sources]
            return list
        return []

    def print(self):

        print('\n\n\n')
        cs.print_header('# Topic ->')
        print(self.topic)

        cs.print_header('# Link ->')
        print(self.link)

        cs.print_header('# Content ->')
        print(self.get_content())

        cs.print_header('# Date ->')
        print(self.date)

        # cs.print_header('# Paragraphs ->')
        # print(self.paragraphs)

        cs.print_header('# Images ->')
        for img in self.img:
            print(img)

        cs.print_header('# Paragraphs + Entities ->')
        for p_enty, p_index in zip(self.entities, range(len(self.entities))):
            cs.print_green('  * Paragraph ' + str(p_index))
            print(self.paragraphs[p_index])
            for entity in p_enty:
                if len(entity) > 0:
                    print(entity[0])

        cs.print_header('# Realated ->')
        for related in self.related:
            print(related)

        cs.print_header('# Sources ->')
        for source in self.sources:
            print(source)


def found_link(list):
    try:
        link = list['href']
        if link:
            return link
        else:
            return ''
    except:
        return ''


def get_str_date(str_date):
    if len(str_date) == 3:
        return str2time(str_date[2])
    return 0


def img_link_correction(link):
    if not link.startswith('http'):
        return 'https:' + link
    return link
