from load_json import *
import itchat
from copy import deepcopy as copy
import random

USER_DICT = {} # user_id, list of interested places

def main():
    itchat.auto_login(hotReload=True, enableCmdQR=2)

    data = Data()
    data_dict == copy(data.data_dict)
    while True:
        time.sleep(10 + 0 * random.random())
        response = load_response()
        if response['data']['areaList'] != data.response['data']['areaList']:
            data.update()
        diff_dict = {k:v for k, v in data.data_dict.items() if k not in data_dict or v != data_dict[k]}
        for user, interests in USER_DICT:
            message = '您关注的地区有如下变化：\n'
            for interest in interests:
                if interest in diff_dict:
                    message += '{}    疑似：{} 确诊：{} 治愈：{} 死亡：{}'.format(interest, *diff_dict[interest])
            if '疑似' in message:
                send_message(user, message)
    
    def send_message(user, message):
        itchat.send(message, user)

if __name__ == '__main__':
    main()

湖北省武汉市
湖北省黄石市、襄樊市
湖北省十堰市、荆州市、宜昌市
湖北省荆门市、鄂州市、孝感市
湖北省黄冈市、咸宁市、随州市
湖北省恩施土家族苗族自治州、仙桃市、神农架林区
