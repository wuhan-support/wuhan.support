import requests
import json
import csv
import os


def load_response():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    api = 'https://server.toolbon.com/home/tools/getPneumonia'
    return json.loads(requests.get(api, headers=headers).text)

class Data(object):
    def __init__(self):
        response =  load_response()
        self.area_stat = response['data']['areaList']
        self.provinces = self.load_stat()
        self.time_stamp = response['data']['statistics']['modifyTime']
        self.suspect = sum([province.suspect for province in self.provinces])
        self.confirmed = sum([province.confirmed for province in self.provinces])
        self.cured = sum([province.cured for province in self.provinces])
        self.dead = sum([province.dead for province in self.provinces])

    def load_stat(area_stat):
        return [Province(province_stat) for province_stat in self.area_stat]
    
    def update():
        area_stat = load_response()['data']['areaList']
        if area_stat != self.area_stat:
            self.provinces = self.load_stat()
            self.time_stamp = time.time()
            with open(os.path.join('./data', str(time_stamp)), 'w+') as f:
                json.dump(response, f)
    
    def write_json(file_name=os.path.join('./jsons', str(time_stamp))):
        with open(file_name, 'w+') as f:
            json.dump(response, f)

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

    def load_stat(province_stat_cities):
        return [City(city_stat) for city_stat in province_stat_cities]

class City(object):
    def __init__(self, city_stat):
        self.name = city_stat['cityName']
        self.suspect = city_stat['suspectedCount']
        self.confirmed = city_stat['confirmedCount']
        self.cured = city_stat['curedCount']
        self.dead = city_stat['deadCount']
