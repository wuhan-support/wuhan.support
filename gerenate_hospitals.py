# -*- coding: UTF-8 -*-
import os
import time
import csv


def read(filename='./hospitals.csv', encoding='utf-8'):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        hospitals = [hospital for hospital in reader]
    return hospitals

def write_md(hospital):
    path = 'test/{}.md'.format(hospital[0])
    md = gerenate_md(hospital)
#     if os.path.exists(path):
#         return
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(md)

def gerenate_md(hospital):
    md = ''
    md += gerenate_header(hospital)
    md += '\n'
    md += gerenate_intro(hospital)
    md += '\n'
    md += gerenate_table(hospital)
    md += '\n'
    md += gerenate_contacts(hospital)
    md += '\n'
    return md        

def gerenate_header(hospital):
    header = '---\n'
    header += 'title: {}\n'.format(hospital[4])
    header += 'summary: {}\n'.format(hospital[5])
    header += 'authors: \n'
    for author in hospital[1].split('|'):
        header += '    - {}\n'.format(author)
    header += 'date: {}\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    header += 'categories: \n    - 捐赠\n'
    header += 'tags: \n    - 捐赠\n'
    header += 'province: {}\n'.format(hospital[2])
    header += 'city: {}\n'.format(hospital[3])
    header += '---\n'
    return header

def gerenate_intro(hospital):
    intro = ''
    for s in hospital[6].split('\\'):
        intro += s
        intro += '\n\n'
    return intro[:-1]

def gerenate_table(hospital):
    table = '|  防护物资（耗材）  |  标准/要求  |\n|------------------|-----------|\n'
    for supply, standard in zip(hospital[11].split('|'), hospital[12].split('|')):
        table += '|  {}  |  {}\n'.format(supply, standard)
    return table

def gerenate_contacts(hospital):
    contacts = ''
    contacts += '地址：{}\n\n'.format(hospital[7])
    if hospital[8]:
        contacts += '电话：{}\n\n'.format(hospital[8])
    contacts += '联系人：\n\n'
    for contact, mobile in zip(hospital[9].split('|'), hospital[10].split('|')):
        contacts += '+ {} {}\n'.format(contact, mobile)
    return contacts[:-1]

if __name__ == '__main__':
    hospitals = read()
    for hospital in hospitals[1:]:
        write_md(hospital)
