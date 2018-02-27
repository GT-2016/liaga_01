#!/usr/bin/python
# -*- coding: utf8 -*-
import random
import struct
from Crypto.Cipher import AES
import hmac
import hashlib
import binascii
import time
import string
import sys
import datetime
#  AES CBC PKCS7padding
BS = 16
def pad(s):
    if len(s) % BS:
        s = s + (BS - len(s)%BS) * chr(BS - len(s)%BS)
    return s
unpad = lambda s : s[0:-ord(s[-1])]
# 随机数组生成
def random_arr(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list 
# 异或操作
def listXor(list1,list2):
    orxlist = []
    for i in range(0,len(list2)):
        rst = list1[i] ^ list2[i]
        result = orxlist.append(rst)
    return orxlist
# 随机字符串生成
def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
def random_hex(y):
    return ''.join(random.choice('0123456789') for x in range(y*2))
# 字节流解包成数组列表
def unpack_list(str):
    return list(struct.unpack('%dB'%len(str), str))
# 8字节转整数
def unpack_int(list):
    return struct.unpack('!Q',list)
# 数组打包成字节流
def pack_bin(arr):
    return struct.pack('%dB'%len(arr), *arr)
# 字符串打包成字节流
def pack_str(str):
    return struct.pack('%ds'%len(str), str)
# 整数打包成8字节流
def pack_int(int):
    return struct.pack('!Q', int)
# 长度整数转两个字节
def len2bit(length):
    len_low = length & 0xff
    len_high = (length & 0xff00) >> 8
    return [len_high, len_low]
# 2字节转长度整数
def bit2len(list):
    return (list[0] << 8) + list[1]
# 解密
def aes_decrypt(key, data):
    iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]           
    aes_object = AES.new(pack_bin(key), AES.MODE_CBC, pack_bin(iv))         
    return aes_object.decrypt(data)
# 加密
def aes_encrypt(key, data):
    iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]           # 16个0，随机向量
    aes_object = AES.new(pack_bin(key), AES.MODE_CBC, pack_bin(iv))         # AES 创建对象
    return aes_object.encrypt(pad(data))
# hmac-sha256值
def hmac_sha256(key, req):
    # print '__algorithm__ :  hmac_sha256 '
    hmac256 = hmac.new(pack_bin(key), pack_bin(req), digestmod=hashlib.sha256).digest()
    return hmac256
# 密码sha256哈希值
def psd_sha256(psd):
    psd_sha256_hex = hashlib.sha256(psd).hexdigest()
    return binascii.unhexlify(psd_sha256_hex)
# 返回时间戳
def timeprt():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
# 打印信息封装，包括时间、文件名、行数
def printMsg(msg):
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
        print u'当前时间：%s,[文件名]-%s,[行号]-%s, ' % (timeprt(), f.f_code.co_filename.split('\\')[4], str(f.f_lineno)),msg
# print timeprt()
# B = [02,9]
# printMsg(u'hihi %s'%B)

# 10进制数组转普通字符串
def arr2str(arr):
    return ''.join(chr(x) for x in arr)
    # map(ord,a)
# 把10进制数组转为16进制字符串
def arr2hex(arr):
    return binascii.hexlify(arr2str(arr))
# 把普通字符串转为10进制数组
def str2arr(str):
    arr = []
    for x in str:
        arr.append(ord(x))
    return arr
# 普通字符串转16进制字符串
def str2hex(str):
    return binascii.hexlify(str)
# 16进制字符串转10进制数组
def hex2arr(hex):
    list = []
    while len(hex) > 1:
        list.append(int(hex[0:2],16))
        hex = hex[2:len(hex)]
    return list

# 16进制字符串转字符串
def hex2str(hex):
    str = ''
    while len(hex) > 1:
        str += chr(int(hex[0:2],16))
        hex = hex[2:len(hex)]
    return str

# req_authkey_id = '13676ad3f0f841b3'
# req_authkey_value = 'd1a91b44523147daa6800903e3067154'

# a = '13676ad3f0f841b3'
# print str2arr(a)
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
# --------报文解析--------------
def msg2Arr():
    print u'# ----------------------------报文解析 ---------------------------#'
    msg ='C93AA0000105200100000000000187A400000000000187A3B2D2222DCB0E42FBB654CC84B7E74241B82B9CA9BCA14198A691C910CA8EB33DD0BBB85E789B417AB49D99B06E106DD303A0CAE78B2D4EDB9D3C82F3E650F7ED2B183452761D4359B2C56E4F3775E9C30A407D330A407933D4C33200484BDAE8F7348ED722E9DF4D'
    print u'报文16进制转10进制数组:',hex2arr(msg) # 报文16进制转10进制数组
    print 'hex2str:',hex2str(msg)
    print u'报文长度:',len(hex2arr(msg)) # 报文长度
def name7pass():
    user_name = 'client_ligg060'        # 字符串用户名
    print 'user_name:',str2arr(user_name)
    psd = '091945003b065c0d0a42'            # 16进制密码
    psd_value = arr2str(encry_keyValue(hex2arr(psd)))
    print 'psd real value:',psd_value
    psd_value_ori = 'qtec@123'          # 字符串密码
    psd_ = arr2hex(encry_keyValue(str2arr(psd_value_ori)))
    # print u'存储时： ',psd_
    # print 'psd hmac',unpack_list(psd_sha256(psd_value))
def keyID7Value():
    root_key_id = '686B454E4C4D59494D71516477797453' # 16进制字符串
    print u'root_key_id 16进制->10数组：',hex2arr(root_key_id) # 16进制->10数组
    
    req_id = []
    key_value = '657423676667366664247161283D3666662E66316B6367635C5C63662877286B'
    print u'root_key_value',arr2hex(encry_keyValue(hex2arr(key_value)))

def lens():
    str = [88, 227, 1, 143, 242, 249, 79, 199, 149, 128, 122, 73, 98, 241, 181, 26, 184, 92, 124, 7, 233, 228, 210, 59, 52, 154, 40, 62, 88, 93, 37, 101, 22, 220, 247, 213, 45, 187, 2, 162, 180, 189, 101, 250, 146, 32, 17, 91, 47, 124, 236, 254, 28, 238, 104, 101, 59, 115, 200, 92, 118, 115, 200, 175, 124, 216, 81, 220, 87, 219, 58, 212, 222, 63, 140, 87, 151, 164, 210, 175, 214, 151, 17, 229, 53, 95, 50, 128, 191, 64, 215, 58, 37, 204, 157, 152, 197, 112, 122, 132, 49, 31, 233, 199, 46, 173, 138, 240, 93, 196, 148, 150, 1, 33, 126, 155, 242, 172, 94, 83, 146, 147, 72, 132, 118, 137, 54, 205, 32, 162, 45, 229, 29, 217, 140, 58, 78, 71, 198, 54, 24, 234, 56, 42, 163, 6, 138, 203, 208, 38, 129, 124, 230, 52, 114, 133, 47, 154, 14, 167, 119, 141, 125, 39, 103, 197, 156, 113, 136, 110, 188, 214, 248, 62, 73, 59, 210, 187, 15, 102, 115, 96, 210, 25, 139, 101, 153, 141, 164, 40, 70]
    print u's length:',len(str)
def float2int(f):
    fs = str(f)
    fa = fs.split('.')
#     print fa
    return fa[0]+fa[1]
# if __name__ == '__main__':
def insert_mysql():
    str1 = 'INSERT INTO `authentication_info` VALUES (\''
    id = '1000201'
    user_name ='node_wgd02'
    phone = 'node_wgd02'
    email = 'node_wgd02'
    user_type = '0'
    password = 'qtec@123'
    status = '0'
    t = time.time()
    t_len= len(float2int(t))/2
    print t_len
#     for i in range(1):
    root_key_id = str2hex(random_char(16))
    print u'真实的root_key_id',root_key_id  
    root_key_value = float2int(t)+str2hex(random_char(32-t_len))
    print u'安全网关root_key_value值（真实值）',root_key_value
    print len(root_key_value)
    root_key_enc = arr2hex(encry_keyValue(hex2arr(root_key_value)))
#     print u'数据库插入root_key_value值（hash之后的）:',root_key_enc
    
    req_authkey_id = str2hex(random_char(16))
    print u'真实的req_authkey_id',req_authkey_id
    req_authkey_value = float2int(t)+str2hex(random_char(32-t_len))
    print u'安全网关req_authkey_value值（真实值）',req_authkey_value
    print len(req_authkey_value)
    req_authkey_enc = arr2hex(encry_keyValue(hex2arr(req_authkey_value)))
#     print u'数据库插入req_authkey_enc值（hash之后的）:',req_authkey_enc
    
    res_authkey_id = str2hex(random_char(16))
    print u'真实的res_authkey_id',res_authkey_id
    res_authkey_value = float2int(t)+str2hex(random_char(32-t_len))
    print u'安全网关res_authkey_value值（真实值）',res_authkey_value
    print len(res_authkey_value)
    res_authkey_enc = arr2hex(encry_keyValue(hex2arr(res_authkey_value)))
#     print u'数据库插入res_authkey_enc值（hash之后的）:',res_authkey_enc
    
    password_value = arr2hex(encry_keyValue(str2arr(password)))
    return str1+ id +'\',\''+user_name+'\',\''+phone+'\',\''+email+'\',\''+user_type+'\',\''+password_value+'\',0x'+root_key_id+',0x'+root_key_enc+',0x'+req_authkey_id+',0x'+req_authkey_enc+',0x'+res_authkey_id+',0x'+res_authkey_enc+',\''+status+'\');'
    # select count(*) from connection_info where user_name like 'client_ligg%'

# print insert_mysql()
# msg2Arr()

def easyE(str):
    return arr2hex(encry_keyValue(str2arr(str)))
def easyD(str):
    return arr2str(encry_keyValue(hex2arr(str)))
# hash之后的转为真实值
def hash2real(h):
    return arr2hex(encry_keyValue(hex2arr(h)))
# print insert_mysql()
origStr = '12'

encStr = 'F7E5E136989E7CE5C949D328A1912CBF'
print hex2str(encStr)
