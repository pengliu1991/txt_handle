#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os
path = "E:\email\Exploit.in" #文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称
new_path = "E:\email\Exploit"
if not os.path.exists(new_path):
        os.makedirs(new_path)
for file in files: #遍历文件夹
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
         f_read = open(path + "\\" + file, 'r')
         f_write = open(new_path + "\\" + file, 'w')
         for line in f_read.readlines():
             line = line.strip()
             if ":" in line:
                 email = line.split(":")[0]
                 f_write.write(email + '\n')
         f_read.close()
         f_write.close()


