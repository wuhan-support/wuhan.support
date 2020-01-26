# -*- coding: UTF-8 -*-
import csv
import os
import time


def read_dir(directory='../data/designated_hospitals'):
    return {filename: read(os.path.join(directory, filename)) for filename in os.listdir(directory) if filename.endswith('.csv')}


def read(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=',')
        hospitals = [hospital for hospital in reader][1:]
    return hospitals


def write_md(name, hospitals):
    path = '../docs/hospitals/{}.md'.format(name[:-4])
    md = gerenate_md(hospitals)
    if os.path.exists(path):
        return
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(md)


def gerenate_md(hospitals):
    md = ''
    md += gerenate_header(hospitals)
    md += '\n'
    md += gerenate_table(hospitals)
    md += '\n'
    return md


def gerenate_header(hospitals):
    hospital = hospitals[:][1]
    header = '---\n'
    header += 'title: {}发热门诊定点机构\n'.format(hospital[2])
    header += 'summary: {}发热门诊定点机构\n'.format(hospital[2])
    header += 'authors: \n'
    for author in hospital[1].split('、'):
        header += '    - {}\n'.format(author)
    header += 'date: {}\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    header += 'categories: \n    - 发热门诊定点机构\n'
    header += 'tags: \n    - 发热门诊定点机构\n'
    header += 'province: {}\n'.format(hospital[2])
    header += 'city: {}\n'.format(hospital[3])
    header += 'suburb: {}\n'.format(hospital[4])
    header += '---\n'
    return header

def gerenate_table(hospitals):
    
    try:
        hospitals[:][1][7]
        table = '|  城市  |  区/县  |  名称  |  地址  |  电话  |\n|------|-------|------|------|------|\n'
        string = '|  {}  |  {}  |  {}  |  {}  |  {}  \n'
    except IndexError:
        table = '|  城市  |  区/县  |  名称  |  地址  |\n|------|-------|------|------|\n'
        string = '|  {}  |  {}  |  {}  |  {}  \n'
    for hospital in hospitals[:]:
            table += string.format(*hospital[3:])
    return table


if __name__ == '__main__':
    hospitals_dict = read_dir()
    for name, hospitals in hospitals_dict.items():
        write_md(name, hospitals)
