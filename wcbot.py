from load_json import *
import itchat
from copy import deepcopy as copy
import random

USER_DICT = {} # user_id, list of interested places

def main():
    itchat.auto_login(hotReload=True, enableCmdQR=1)

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
