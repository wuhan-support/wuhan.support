import requests
import json
import csv
import os
import time
import random

def load_response():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
        api = 'https://server.toolbon.com/home/tools/getPneumonia'
        response = json.loads(requests.get(api, headers=headers).text)
        if not response['data']['statistics']['modifyTime'] or not response['data']['areaList']:
            raise Exception('no data received')
        return response
    except Exception:
        import pdb; pdb.set_trace()
        return load_response()


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
            self.provinces = self.load_stat(self.response['data']['areaList'])
            self.time_stamp = self.response['data']['statistics']['modifyTime']
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

            self.write_json()
        except Exception as e:
            import pdb; pdb.set_trace()
            time.sleep(10 + 10 * random.random())
            self.init()

    def update(self):
        self.response = load_response()
        self.init()
        print('data updated at {}'.format(data.time_stamp))
    
    def write_json(self, file_name=None):
        if not file_name:
            file_name = './jsons/{}.json'.format(self.time_stamp)
        with open(file_name, 'w+') as f:
            json.dump(self.response, f)

class Province(object):
    def __init__(self, province_stat):
        self.name = province_stat['provinceName']
        self.abbreviation = province_stat['provinceShortName']
        self.suspect = province_stat['suspectedCount']
        self.confirmed = province_stat['confirmedCount']
        self.cured = province_stat['curedCount']
        self.dead = province_stat['deadCount']
        self.cities = self.load_stat(province_stat['cities'])
        self.comment = province_stat['comment']

    def load_stat(self, province_stat_cities):
        return [City(city_stat) for city_stat in province_stat_cities]

class City(object):
    def __init__(self, city_stat):
        self.name = city_stat['cityName']
        self.suspect = city_stat['suspectedCount']
        self.confirmed = city_stat['confirmedCount']
        self.cured = city_stat['curedCount']
        self.dead = city_stat['deadCount']

if __name__ == "__main__":
    data = Data()

    while True:
        time.sleep(10 + 0 * random.random())
        response = load_response()
        if response['data']['areaList'] != data.response['data']['areaList']:
            data.update()
