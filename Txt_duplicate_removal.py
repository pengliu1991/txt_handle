#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')

mongo_conn = MongoClient('mongodb://192.168.20.42:27017')
mongo_db = mongo_conn['facebook_email']

read_path = r"E:\email\Exploit\1.txt"
write_path = "C:\Users\upeng\Desktop\email.txt"
f_read = open(read_path, 'r')
f_write = open(write_path, 'w')
for line in  f_read.readlines():
    line = line.strip()
    print line
    email_find = mongo_db.fb_email.find_one({"email_account": str(line)})
    if email_find == None:
        f_write.write(line + '\n')
        print "写入成功"
    else:
        pass
f_read.close()
f_write.close()