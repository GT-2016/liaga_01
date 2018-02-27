# -*- coding: utf8 -*-
'''

'''
import os,sys
import binascii
import shelve       # 数据存储--字典
import struct
import MySQLdb
#    定义全局变量
# data = ''
# data_hex =''
# j=0
random_num=1
IP =  ['10.64.121.1', '10.64.121.2']
Name = 'root'
Passwd = 'Qtec_KSM*'
dataBase = 'QkPool'
raw_num = 32
# encry_keyValue传入参数为数组
def encry_keyValue(keyValue):
    j = 0
    newKeyValue = []
    str1 = "g?ol0d!en@s7ec.1u8r$ityf*e#rr3*yw&a^y"
    str2 = "3g!#d34&fddf*d4adfd8)de+^dad*d57#daTga"
    str3 = "*dne71#dc&ia?yad>lad,ad3h*aducat3~da3)d"
    str4 = "-vdg9e*dqa1cF?Ka3,d3emca*^1p)u5i]ag2r*de"
    for i in range(len(keyValue)):
        # print 'i:',i
        if (i % 2) == 0:
            if (i % 5) == 0:
                newKeyValue.append(keyValue[i] ^ ord(str1[j]))
            else:
                newKeyValue.append(keyValue[i] ^ ord(str2[j]))
        else:
            if (i % 3) == 0:
                newKeyValue.append(keyValue[i] ^ ord(str3[j]))
            else:
                newKeyValue.append(keyValue[i] ^ ord(str4[j]))
        j+=1
        if j > 36:
            j = 0
    return newKeyValue

# 16进制字符串转10进制数组
def hex2arr(hex):
    list = []
    while len(hex) > 1:
        list.append(int(hex[0:2],16))
        hex = hex[2:len(hex)]
    return list

# 10进制数组转普通字符串
def arr2str(arr):
    return ''.join(chr(x) for x in arr)
# 把10进制数组转为16进制字符串
def arr2hex(arr):
    return binascii.hexlify(arr2str(arr))
# 普通字符串转16进制字符串
def str2hex(str):
    return binascii.hexlify(str)
def unpack_list(str):
    return list(struct.unpack('%dB'%len(str), str))
def pack_bin(arr):
    return struct.pack('%dB'%len(arr), *arr)
# ---------随机数文件random打头【有规律的文件名】，切割成特定大小的文件
def random_split(file_num, size):
    j=0
    for i in range(file_num):
        fname = "random%d"%(i+1)
        f = open(fname,'rb')  
        while True:
            buff = f.read(size*1024)
            j=j+1
            filename = "random/random%d"%(i+1) +"__%d"%j + ".dat"       # 存储路径
    #         print filename
            file = open(filename,'wb')
            file.write(buff)
            if not buff:
                break 
# ---------file_size 截取一个sql或者txt文件 大小为size--------------------#
def file_size(file_name, size, path):
    j=0
    while True:
        buff = file_name.read(size*1024)
        j=j+1
        filename = path +'/' + path + '_%d'%j + ".dat"
        files = open(filename,'wb')
        files.write(buff)
        if not buff:
            break  
# --------从数据库中将所有的生成表中的key_value取出来 ---------------#
def mysql_raw(ip, name, passwd, database):
    data = ''
    num = 0
#     file_raw = open('mysql_rawAll.txt','wb')
    for i in range(len(ip)):
        db = MySQLdb.connect(ip[i], name, passwd, database)        # 打开数据库连接
        cursor = db.cursor()        # 使用cursor()获取操作游标
        for j in range(raw_num):
            cursor.execute('select hex(key_value) from raw_key_%d'%j)
            while True:
                data_one = cursor.fetchone()
#                 print data_one
                if not data_one:
                    break
                data_one = pack_bin(encry_keyValue(hex2arr(data_one[0]))) + '\n'         # 解密转成字节流
#                 data_one = arr2hex(encry_keyValue(hex2arr(data_one[0]))) + '\n'         # 解密
                data+= data_one
                num+=1
#                 print data
            
            file_raw.write(data)
#         file_raw.close()
    print 'all data number: ',num

if __name__ == '__main__':
    #-----------------------QKD产生的密钥----------------------#
# #     f = open('data.sql','r')
#     f = open('data/test109.txt','r')
#     file = open('test1.dat','wb')
#     #-------从sql中读取--------------#
#     s = f.readlines()        # 读取行
#     for line in s:
# #         fsp = line.split('\'')      # sql解析，根据不同的select结果而不同
#     #     print len(data)
#     #     print fsp[1]
# #         raw = pack_bin(encry_keyValue(hex2arr(fsp[1])))  # sql解析后--解密函数
#         raw= pack_bin(encry_keyValue(hex2arr(line)))  # 解密函数
#         file.write(raw)
#     #     break
#     file_w = open('test1.dat','rb')
#     file_size(file_w, 128, 'qkd')
    file_raw = open('mysql_rawAll.txt','wb')
    mysql_raw(IP, Name, Passwd, dataBase)
    files = open('mysql_rawAll.txt','rb')
    file_size(files, 128, 'qkd')    # 需要自己创建qkd文件夹

#-----------------读取random1文件，转存为16进制的txt文件--------------#

# f = open('random1','rb')
# file = open('random1_str.txt','w')

# s = f.readlines()
# for line in s:
#     raw = unpack_list(line)     # 将二进制字节流转为普通字符
#     data = arr2hex(raw)        # 将普通字符转为字节流
#     file.write(data)    # 边读边写
# print data
# print len(data)

#--------------------按字节数读取文件-------------------#

#     random_split(random_num, 128)

print '~finished~'
# file.close()        # 一般为写函数
# f.close()       # 一般为读函数

