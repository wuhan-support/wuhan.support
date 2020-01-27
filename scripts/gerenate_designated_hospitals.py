# -*- coding: UTF-8 -*-
import csv
import os
import time

import pypinyin as py


def read_dir(directory='../data/designated_hospitals'):
    return {filename: read(os.path.join(directory, filename)) for filename in os.listdir(directory) if
            filename.endswith('.csv')}


def read(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=',')
        hospitals = [hospital for hospital in reader][1:]
    return hospitals


def write_md(name, hospitals):
    path = '../docs/hospitals/{}.md'.format(name[:-4])
    md = gerenate_md(hospitals, name[:-4])
    if os.path.exists(path):
        return
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(md)


def gerenate_md(hospitals, name):
    md = '{}\n{}\n'.format(gerenate_header(hospitals[:][1]), gerenate_table(hospitals, name))
    return md


def gerenate_header(hospital, title_index=2):
    header = '---\n'
    header += 'title: {}发热门诊定点机构\n'.format(hospital[title_index])
    header += 'summary: {}发热门诊定点机构\n'.format(hospital[title_index])
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


def gerenate_table(hospitals, name):
    province_dir = '../docs/hospitals/{}'.format(name)
    try:
        hospitals[:][1][7]
        table = '|  城市  |  区/县  |  名称  |  地址  |  电话  |  导航  |\n|------|-------|------|------|------|------|\n'
        string = '|  {}  |  {}  |  {}  |  {}  |  {}  |  {}  \n'
    except IndexError:
        table = '|  城市  |  区/县  |  名称  |  地址  |  导航  |\n|------|-------|------|------|------|\n'
        string = '|  {}  |  {}  |  {}  |  {}  |  {}  \n'
    city = ''
    city_hospitals = []
    hospitals_len = len(hospitals)
    for index, hospital in enumerate(hospitals[:]):
        hospital.append('[🧭](https://ditu.amap.com/search?query={})'.format(hospital[5]))
        table += string.format(*hospital[3:])
        if not city:
            city = hospital[3]
            city_hospitals.append(hospital)
        # ensure the info of last iter
        elif index == hospitals_len - 1:
            gerenate_city(city_hospitals, province_dir, city)
        elif city == hospital[3]:
            city_hospitals.append(hospital)
        else:
            gerenate_city(city_hospitals, province_dir, city)
            city = ''
            city_hospitals = []

    return table


def gerenate_city(city_hospitals, province_dir, city):
    suburb = ''
    suburb_hospitals = []
    # 怎么杨移除xx族自治州？
    if city.endswith(('新区')):
        city_name = ''.join(py.lazy_pinyin(city, style=py.Style.NORMAL)[:-2])
    elif city.endswith(('市', '州','区', '县')):
        city_name = ''.join(py.lazy_pinyin(city, style=py.Style.NORMAL)[:-1])
    else:
        city_name = ''.join(py.lazy_pinyin(city, style=py.Style.NORMAL)[:-1])
    city_path = os.path.join(province_dir, '{}.md'.format(city_name))
    if not os.path.exists(city_path):
        if not os.path.isdir(province_dir):
            os.makedirs(province_dir)
        try:
            hospitals[:][1][7]
            city_table = '|  区/县  |  名称  |  地址  |  电话  |  导航  |\n|------|-------|------|------|------|\n'
            city_string = '|  {}  |  {}  |  {}  |  {}  |  {}  \n'
        except IndexError:
            city_table = '|  区/县  |  名称  |  地址  |  导航  |\n|------|-------|------|------|\n'
            city_string = '|  {}  |  {}  |  {}  |  {}  \n'
        for city_hospital in city_hospitals:
            city_hospital.append('[🧭](https://ditu.amap.com/search?query={})'.format(city_hospital[5]))
            city_table += city_string.format(*city_hospital[4:])

        with open(city_path, 'w+', encoding='utf-8') as f:
            f.write('{}\n{}\n'.format(gerenate_header(city_hospitals[0], 3), city_table))

   


if __name__ == '__main__':
    hospitals_dict = read_dir()
    for name, hospitals in hospitals_dict.items():
        write_md(name, hospitals)
