# -*- coding: UTF-8 -*-
import json
import os
import time


def read(filename='../data/accommodations.json', encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        return json.load(f)


def dict_process(j):
    d = dict()
    for item in list(j.values())[0]:
        if item['province'] and item['city'] and item['suburb']:
            if item['province'] not in d.keys():
                d[item['province']] = dict()
            if item['city'] not in d[item['province']].keys():
                d[item['province']][item['city']] = dict()
            if item['suburb'] not in d[item['province']][item['city']].keys():
                d[item['province']][item['city']][item['suburb']] = list()
            d[item['province']][item['city']][item['suburb']].append(item)
    return d


def write_md(hotel, root = '../docs/hotels/'):
    j = read()
    d = dict_process(j)
    for key, value in d.items():



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
    write_md()
