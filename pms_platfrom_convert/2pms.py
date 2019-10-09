#!/usr/bin/python
# encoding: utf-8 

import sys
import csv
import os
import argparse

temp={}

def _argparse():
    parser=argparse.ArgumentParser(description='script for convert cvs ,import to pms')
    parser.add_argument('-f',action='store',dest='filename',help='csv filename import')
    parser.add_argument('-P', dest='P_ID', help='Product ID',type=int)
    parser.add_argument('-p',dest='p_ID',help='platfrom ID')
    return parser.parse_args()

def platform_check(pID):
    p={'x86_64':'3','Loongson':'4','SW64':'7','ARM':'13'}
    str=''
    for i in p.keys():
        if ( pID.lower() in i.lower()) or ( pID == p.get(i)):
            str='%s(#%s)'%(i,p.get(i))
            break;
    if len(str) == 0: 
        sys.stdout.write("platform input error %s\n"%pID)
    return str

def templete():
    try:
        reader=csv.reader(open('templet.csv','r'))
        for list in reader:
            mstr=list[1].split('(')[0]
            nid=list[1].split('#')[-1].strip(')')
            temp[mstr]=nid
    except OSError as reason :
        sys.stdout.write("templet.csv open failed,please check the file\n")

def moudle_check(dpid,mstr):
    moudle=''
    spid=mstr.split('/')[1]
    str=mstr.split('(')[0].replace(spid,dpid)
    if temp.has_key(str):
        moudle=str+'(#'+temp.get(str)+')'
    else :
       sys.stdout.write("%s on pms.deepin.cn is not exist\n"%str)
    return moudle

def convert(filename,pID):
    destfile=pID.split('(')[0]+filename
    reader=csv.reader(open(filename,'rb'))
    open(destfile,'w+').truncate()
    writer=csv.writer(open(destfile,'a+'))
    res=[]
    for list in reader:
        res.append(list)
    writer.writerow(res[0])
    for list in res[1:]: 
        list[0]=0
        list[2]=pID
        list[3]=moudle_check(pID.split('(')[0],list[3])
        if list[11].strip() == '':
            list[11] = '3'
        writer.writerow(list)

def moudle_convert(mstr):
    moudle=''
    str=mstr.split('(')[0]
    if temp.has_key(str):
        moudle=str+'(#'+temp.get(str)+')'
    else :
       sys.stdout.write("%s on pms.deepin.cn is not exist\n"%str)
    return moudle

def Product_convert(filename, P_ID) :
    destfile=str(P_ID)+filename
    reader=csv.reader(open(filename,'rb'))
    open(destfile,'w+').truncate()
    writer=csv.writer(open(destfile,'a+'))
    res=[]
    for list in reader:
        res.append(list)
    writer.writerow(res[0])
    for list in res[1:]:
        list[0]=0
        list[1]='(#'+str(P_ID)+')'
        list[2]=moudle_convert(list[2])
        if list[11].strip() == '':
            list[11] = '3'
        writer.writerow(list)


def main():
    parser=_argparse()
    if parser.p_ID :
        pID=platform_check(parser.p_ID)
        templete()
        if len(pID) > 0:
            convert(parser.filename,pID)
    if parser.P_ID :
        templete()
        Product_convert(parser.filename,parser.P_ID)

if __name__=='__main__':
    main()
