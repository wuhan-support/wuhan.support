# -*- coding: UTF-8 -*-
import csv
import os
import time


def read(filename='../data/hotels.csv', encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=',')
        hotels = [hotel for hotel in reader]
    return hotels


def write_md(hotel):
    path = '../docs/hotels/{}.md'.format(hotel[0])
    md = gerenate_md(hotel)
    if os.path.exists(path):
        return
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(md)


def gerenate_md(hotel):
    md = ''
    md += gerenate_header(hotel)
    md += '\n'
    md += gerenate_intro(hotel)
    md += '\n'
    md += gerenate_contacts(hotel)
    md += '\n'
    return md


def gerenate_header(hotel):
    header = '---\n'
    header += 'title: {}\n'.format(hotel[5])
    header += 'summary: {}\n'.format(hotel[6])
    header += 'authors: \n'
    for author in hotel[1].split('、'):
        header += '    - {}\n'.format(author)
    header += 'date: {}\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    header += 'categories: \n    - 捐赠\n'
    header += 'tags: \n    - 捐赠\n'
    header += 'province: {}\n'.format(hotel[2])
    header += 'city: {}\n'.format(hotel[3])
    header += 'suburb: {}\n'.format(hotel[4])
    header += '---\n'
    return header


def gerenate_intro(hotel):
    intro = '## {} {} {}\n## {}\n## {}'.format(*hotel[2:7])
    for s in hotel[12].split('\\'):
        intro += s
        intro += '\n\n'
    return intro[:-1]


def gerenate_contacts(hotel):
    contacts = ''
    if hotel[8]:
        contacts += '##床位数：{}\n\n'.format(hotel[8])
    if hotel[9]:
        contacts += '##联系方式：{}\n\n'.format(hotel[9])
    if hotel[10] and hotel[11]:
        contacts += '##联系人：\n\n'
        for contact, mobile in zip(hotel[10].split('、'), hotel[11].split('、')):
            contacts += '+ {} {}\n'.format(contact, mobile)
    return contacts[:-1]


if __name__ == '__main__':
    hotels = read()
    for hotel in hotels[1:]:
        write_md(hotel)
