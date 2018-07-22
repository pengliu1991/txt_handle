#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd, json, sys
from datetime import datetime
from xlrd import xldate_as_tuple

reload(sys)
sys.setdefaultencoding('utf-8')

#json_file = u'C:\\Users\\upeng\\Desktop\\资质证书.json'
excl_file = u'C:\\Users\\upeng\\Desktop\\实验室数据统计.xlsx'
#data = xlrd.open_workbook(excl_file)
workbook = xlrd.open_workbook(excl_file)
list = workbook.sheet_names()
for name in list:
    print name
    json_file_name = 'C:\\Users\\upeng\\Desktop\\实验室数据统计\\' + str(name) + ".json"
    json_file = json_file_name.decode("utf8")
    table = workbook.sheet_by_name(name)
#table = data.sheets()[0]

    nrows = table.nrows #行数
    ncols = table.ncols #列数
    #print ncols
    titleValues= table.row_values(0)
    d_json = {}
    ofile = open(json_file, 'w')

    ofile.write("[")
    ofile.write("\n")
    for i in xrange(1,nrows):
        rowValues= table.row_values(i) #某一行数据
        for j in range(ncols):
            ctype = table.cell(i, j).ctype
            #print ctype
            if ctype == 2 and rowValues[j] % 1 == 0:
                d_json[titleValues[j]] = str(int(rowValues[j]))
            elif ctype == 3:
                date = datetime(*xldate_as_tuple(rowValues[j], 0))
                rowValues[j] = date.strftime('%Y/%m/%d')
                d_json[titleValues[j]] = str(rowValues[j])
            else:
                d_json[titleValues[j]] = str(rowValues[j])
            # if ctype == 2 and rowValues[j] % 1 == 0:
            #     d_json[titleValues[j]] = str(int(rowValues[j])
            # elif ctype == 3:
            #     date = datetime(*xldate_as_tuple(rowValues[j], 0))
            #     cell = date.strftime('%Y/%d/%m %H:%M:%S')

            # if titleValues[j] == u"编号" or titleValues[j] ==u"证书号" or titleValues[j] == u"颁发日期" or titleValues[j] == u"年份" or titleValues[j] == u"出版时间" or titleValues[j] == u"发表日期":
            #     d_json[titleValues[j]] = str(int(rowValues[j]))
            # else:
            #     d_json[titleValues[j]] = str(rowValues[j])
        data_json = json.dumps(d_json, ensure_ascii=False, encoding='utf-8', indent=4)
        for line in data_json:
            ofile.write(line)
        if i+1 < nrows:
            ofile.write(",")
            ofile.write("\n")
        else:
            ofile.write("\n")
    ofile.write("]")