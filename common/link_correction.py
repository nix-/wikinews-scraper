#!/usr/bin/python


def correct_entity_link(entity):
    if entity[0] != '':  # and entity[0] != 'Share it!':
        if not entity[1].startswith('http'):
            entity[1] = 'https://en.wikipedia.org' + entity[1]

    return entity


def link_correction(link):

    if not link.startswith('http'):
        link = 'https:/' + link

    return link
