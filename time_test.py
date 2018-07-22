#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
pastTime = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')#过去一小时时间
afterTomorrowTime = (datetime.datetime.now()- datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')#后天
tomorrowTime = (datetime.datetime.now()- datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')#明天
print('\n',nowTime,'\n',pastTime,'\n',afterTomorrowTime,'\n',tomorrowTime)