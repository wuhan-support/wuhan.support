import json
import random
import time

import requests


def load_response():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4037.2 Safari/537.36',
            'Connection': 'keep - alive',
            'Cache-Control': 'max-age=360',
            'Upgrade-Insecure-Requests': '1',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-AU;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'Host': 'service-f9fjwngp-1252021671.bj.apigw.tencentcs.com'
        }
        api = 'https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia'
        response = json.loads(requests.get(api, headers=headers).text)
        if not response['data']['listByArea']:
            raise Exception(response)
        print('json loaded at time {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return response
    except Exception as e:
        print(e)
        print('json load failed, waiting for around 15 seconds')
        time.sleep(15 + 5 * random.random())
        return load_response()


def load_json(file_name='./jsons/latest.json'):
    with open(file_name, 'r+') as f:
        return json.load(f)


def write_json(file_name, js):
    with open(file_name, 'w+') as f:
        json.dump(js, f)


class Data(object):
    def __init__(self):
        self.response = load_response()
        self.provinces = []
        self.time_stamp = 0
        self.suspect = 0
        self.confirmed = 0
        self.cured = 0
        self.dead = 0
        self.data_dict = {}
        self.init()

    def load_stat(self, area_stat):
        return [Province(province_stat) for province_stat in area_stat]

    def init(self):
        try:
            self.provinces = self.load_stat(self.response['data']['listByArea'])
            self.time_stamp = time.time()
            self.suspect = 0
            self.confirmed = 0
            self.cured = 0
            self.dead = 0
            self.data_dict = {}
            for province in self.provinces:
                self.suspect += province.suspect
                self.confirmed += province.confirmed
                self.cured += province.cured
                self.dead += province.dead
                self.data_dict[province.name] = [province.suspect, province.confirmed, province.cured, province.dead]
                for city in province.cities:
                    self.data_dict[city.name] = [city.suspect, city.confirmed, city.cured, city.dead]
            latest_response = load_json()
            if latest_response['data']['listByArea'] != self.response['data']['listByArea']:
                write_json('./jsons/{}.json'.format(self.time_stamp), self.response)
                write_json('./jsons/latest.json', self.response)
        except Exception as e:
            print(e)
            print('data construction failed')
            time.sleep(15 + 10 * random.random())
            self.init()

    def update(self):
        self.response = load_response()
        self.init()
        print('data updated at {}'.format(data.time_stamp))


class Province(object):
    def __init__(self, province_stat):
        self.name = province_stat['provinceName']
        self.abbreviation = province_stat['provinceShortName']
        self.suspect = province_stat['suspected']
        self.confirmed = province_stat['confirmed']
        self.cured = province_stat['cured']
        self.dead = province_stat['dead']
        self.cities = self.load_stat(province_stat['cities'])
        self.comment = province_stat['comment']

    def load_stat(self, province_stat_cities):
        return [City(city_stat) for city_stat in province_stat_cities]


class City(object):
    def __init__(self, city_stat):
        self.name = city_stat['cityName']
        self.suspect = city_stat['suspected']
        self.confirmed = city_stat['confirmed']
        self.cured = city_stat['cured']
        self.dead = city_stat['dead']


if __name__ == "__main__":
    data = Data()

    while True:
        time.sleep(45 + 30 * random.random())
        response = load_response()
        if response['data']['listByArea'] != data.response['data']['listByArea']:
            data.update()
