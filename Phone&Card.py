# -*- coding: utf8 -*-
import os
import random
from datetime import datetime,timedelta,date
import re
import time
from compiler.pycodegen import EXCEPT
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#DC_PATH = BASE_DIR  + "districtcode.txt"
DC_PATH = "districtcode.txt"
# 随机生成手机号码
def createPhone():
    prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
    return random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))

# 随机生成身份证号
def getdistrictcode(): 
    with open(DC_PATH) as file: 
        data = file.read() 
        districtlist = data.split('\n') 
    for node in districtlist: 
    #print node 
        if node[10:11] != ' ': 
            state = node[10:].strip() 
        if node[10:11]==' 'and node[12:13]!=' ': 
            city = node[12:].strip() 
        if node[10:11] == ' 'and node[12:13]==' ': 
            district = node[14:].strip() 
            code = node[0:6] 
            codelist.append({"state":state,"city":city,"district":district,"code":code})

def gennerator(): 
    global codelist 
    codelist = [] 
    if not codelist:
        getdistrictcode()
    id = codelist[random.randint(0,len(codelist))]['code'] #地区项 
    id = id + str(random.randint(1930,2017)) #年份项 
    da = date.today()+timedelta(days=random.randint(1,366)) #月份和日期项 
    id = id + da.strftime('%m%d') 
    id = id+ str(random.randint(100,300))#，顺序号简单处理 
  
    i = 0
    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2] #权重项 
    checkcode ={'0':'1','1':'0','2':'X','3':'9','4':'8','5':'7','6':'6','7':'5','8':'5','9':'3','10':'2'} #校验码映射 
    for i in range(0,len(id)):
        count = count +int(id[i])*weight[i] 
    id = id + checkcode[str(count%11)] #算出校验码 
    return id
def isCardID(cardID):
    if len(cardID) == 18:
#         print 'length 18'
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2] #权重项
        checkcode ={'0':'1','1':'0','2':'X','3':'9','4':'8','5':'7','6':'6','7':'5','8':'5','9':'3','10':'2'} #校验码映射
        if re.match('\d|x$', cardID):
#             print 're true'
            sum = 0
            idx = 0
            for i in range(0, len(cardID)-1):
                sum = sum + int(cardID[i]) * int(weight[i])
#                 print 'i: ', i, sum
            idx = sum % 11
            return checkcode[str(idx)] == cardID[17].upper()
        else:
            print '18 length: but not id card '
    elif len(cardID) == 15:
        # 判断月日
        if re.match('\d', cardID):
            month = cardID[8:12]
            print 'year:',month
            try:
                time.strptime(month, "%m%d")
                print '15 length 有效年月'
                print '15 length 校验通过'
            except:
                print '15 length 不是有效年月'
#         print '二代身份证，暂不做校验'     #校验只校验月日
    else:
        return 'false'
for i in range(0,2):
    print  createPhone()
    print gennerator()
# id = '130503670451001'
# isCardID(id)