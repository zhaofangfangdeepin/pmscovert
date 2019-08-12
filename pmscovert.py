#!/usr/bin/python
# encoding: utf-8 

import sys
import csv
import os
import re

armkey=[]
lxl=[]
lxk=[]
lxkey={}
testcase=[]
filename = "测试用例.csv"
for line in open("lx.txt"):
	lxnum=line[-8:]
	lxstr=line[:-8]
	lxl.append(lxstr)
	lxk.append(lxnum)
	lxkey=dict(zip(lxl,lxk))

def file_init():
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "aw") as csv_file:
        fieldnames = ['用例编号', '所属产品','平台','所属模块', '用例标题', '前置条件', '步骤', '预期', '关键词','优先级','用例类型', '适用阶段','用例状态', '结果']
	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	writer.writeheader()


def write_csv(testcases):
    with open( filename, "aw") as csv_file:
        fieldnames = ['用例编号', '所属产品','平台','所属模块', '用例标题', '前置条件', '步骤', '预期', '关键词','优先级','用例类型', '适用阶段','用例状态', '结果']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      	writer.writerow({'所属产品': '桌面专业版(#11)',
                             '平台':'所有平台(#0)',
                             '所属模块': testcases[1],
                             '用例标题': testcases[3],
                             '前置条件': testcases[4],
                             '步骤': testcases[5],
                             '预期': testcases[6],
                             '关键词' :'',
                             '优先级':testcases[9],
                             '用例类型': '功能测试',
                             '适用阶段': '功能测试阶段 集成测试阶段 系统测试阶段 版本验证阶段',
                             '用例状态': '正常'})
def check_write():
    file_init()
    with open('龙芯服务器用例.csv') as f:
        reader = csv.reader(f)
	header_row = next(reader)
	for row in reader:
            mstr=row[1][:-7]
	    #lmstr=mstr.replace('ARM','Loongson')
	    if mstr in lxl:
		    key=lxkey[ mstr ]
		    row[1]=mstr+key
                    write_csv(row)
            else:
                print mstr

def main():
    check_write()

if __name__=='__main__':
    main()
