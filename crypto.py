# -*-coding:UTF-8-*-
#!/usr/bin/python
'''
加密卡接口封装 from 彭文博
调用数据库中的加密密钥，通过该解密接口解密，再将解密后的数据按照128字节分成多个小文件
Date：2018/02/26
'''

import ctypes
from ctypes import *
# import os,random
import binascii
import struct

g_blocksize = ctypes.c_int(16)
SGD_SMS4_CBC = 0x00002002
random_num=1
IP =  ['10.64.121.1', '10.64.121.2']
Name = 'root'
Passwd = 'Qtec_KSM*'
dataBase = 'QkPool'
raw_num = 32

# def random_arr(start, stop, length):
#     start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
#     length = int(abs(length)) if length else 0
#     random_list = []
#     for i in range(length):
#         random_list.append(random.randint(start, stop))
#     return random_list

def hex2arr(hex):
    list = []
    while len(hex) > 1:
        list.append(int(hex[0:2],16))
        hex = hex[2:len(hex)]
    return list

def arr2str(arr):
    return ''.join(chr(x) for x in arr)

def arr2hex(arr):
    return binascii.hexlify(arr2str(arr))

def str2hex(str):
    return binascii.hexlify(str)

def unpack_list(str):
    return list(struct.unpack('%dB'%len(str), str))

def pack_bin(arr):
    return struct.pack('%dB'%len(arr), *arr)

def return_value(arr):
    if hasattr(arr,'value'):
        return arr.value
    else:
        values = []
        length = len(arr)
        for i in range(length):
            values.append(arr[i])
        return values

def file_size(fileName, size, path):
    j=0
    while True:
        buff = fileName.read(size*1024)
        j=j+1
        filename = path +'/' + path + '_%d'%j + ".dat"
        files = open(filename,'wb')
        files.write(buff)
        if not buff:
            break

class CRYPTO(object):
    def __init__(self):
        self.libc = cdll.LoadLibrary('D:\\Python\\sws\\clibs\\swsds.dll')
        self.base = ctypes.c_void_p()
        self.swshandle = ctypes.pointer(self.base)

    def padding(self, inData, inDataLen, blockSize):
        if blockSize <= 0:
            return -1
        paddingLen = blockSize.value - (inDataLen.value % blockSize.value)
        for i in range(0, paddingLen):
            inData[inDataLen.value + i] = paddingLen
        return inDataLen.value + paddingLen

    def getpaddinglen(self, inData, inDataLen):
        return inData[inDataLen.value - 1]

    def opendev(self):
        nRet = self.libc.SDF_OpenDevice(self.swshandle)
        if nRet != 0:
            print "open device error, nRet = ", nRet
            return -1
        return 0

    def closedev(self):
        nRet = self.libc.SDF_CloseDevice(self.base)
        if nRet != 0:
            return -1
        return 0

    def encrypt(self, inData, inDataLen, outData, outDataLen):
        print "====================start encrypt============="
        sessionHanele = ctypes.c_void_p()
        hSessionHandle = ctypes.pointer(sessionHanele)
        #open session
        nRet = self.libc.SDF_OpenSession(self.base, hSessionHandle)
        if nRet != 0:
            print "init error"
            return -1

        #get key handle
        keyhandle = ctypes.c_void_p()
        hkeyhandle = ctypes.pointer(keyhandle)
        nRet = self.libc.SDF_GetSymmKeyHandle(sessionHanele, 1, hkeyhandle)
        if nRet != 0:
            self.libc.SDF_CloseSession(sessionHanele)   #close session
            print "get key handle error, nRet = ", nRet
            return -1

        #padding data
        pdDataLen = self.padding(inData, inDataLen, g_blocksize)
        if pdDataLen <= 0:
            self.libc.SDF_DestroyKey(sessionHanele, keyhandle) #destory key
            self.libc.SDF_CloseSession(sessionHanele)   #close session
            print "padding error"
            return -1

        #encrypt data
        pIv = [0x00] * 16
        Iv = (c_ubyte * 16)(*pIv)
        nRet = self.libc.SDF_Encrypt(sessionHanele, keyhandle, SGD_SMS4_CBC, Iv, inData, pdDataLen, byref(outData),
                                     byref(outDataLen))
        if nRet != 0:
            self.libc.SDF_DestroyKey(sessionHanele, keyhandle) #destory key
            self.libc.SDF_CloseSession(sessionHanele)   #close session
            print "CQtSwsCrypto::SwsEncryptData SDF_Encrypt error! nRet = ", nRet
            return -1

        #destory key handle
        self.libc.SDF_DestroyKey(sessionHanele, keyhandle)

        #close session
        self.libc.SDF_CloseSession(sessionHanele)

        return 0

    def decrypt(self, inData, inDataLen, outData, outDataLen):
        # print "====================start decrypt============="
        sessionHanele = ctypes.c_void_p()
        hSessionHandle = ctypes.pointer(sessionHanele)
        # open session
        nRet = self.libc.SDF_OpenSession(self.base, hSessionHandle)
        if nRet != 0:
            print "init error"
            return -1

        # get key handle
        keyhandle = ctypes.c_void_p()
        hkeyhandle = ctypes.pointer(keyhandle)
        nRet = self.libc.SDF_GetSymmKeyHandle(sessionHanele, 1, hkeyhandle)
        if nRet != 0:
            self.libc.SDF_CloseSession(sessionHanele)  # close session
            print "get key handle error"
            return -1

        # decrypt data
        pIv = [0x00] * 16
        Iv = (c_ubyte * 16)(*pIv)
        nRet = self.libc.SDF_Decrypt(sessionHanele, keyhandle, SGD_SMS4_CBC, Iv, inData, inDataLen, byref(outData),
                                     byref(outDataLen))
        if nRet != 0:
            self.libc.SDF_DestroyKey(sessionHanele, keyhandle)  # destory key
            self.libc.SDF_CloseSession(sessionHanele)  # close session
            print "CQtSwsCrypto::SwsEncryptData SDF_Encrypt error! nRet = ", nRet
            return -1

        # remove padding data
        pdDataLen = self.getpaddinglen(outData, outDataLen)
        outDataLen.value -= pdDataLen

        # destory key handle
        self.libc.SDF_DestroyKey(sessionHanele, keyhandle)

        # close session
        self.libc.SDF_CloseSession(sessionHanele)

        return 0

if __name__ == '__main__':
    crypto = CRYPTO()

    status = crypto.opendev()
    if status != 0:
        print "open device error"
        exit(-1)

    #test encrypt
    #init org buffer
    # ----------------encrypt not used----------------start------#

    # orgData = [0x03] * 48
    # orgData = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]
    # orgDataLen = ctypes.c_int(32)
    # OrgData = (c_ubyte * 48)(*orgData)
    # #init enc bufer
    # encData = [0x00] * 48
    # encDataLen = ctypes.c_int(48)
    # EncData = (c_ubyte * 48)(*encData)
    #
    # status = crypto.encrypt(OrgData, orgDataLen, EncData, encDataLen)
    # if status != 0:
    #     print "encrypt error"
    #     exit(-1)
    # print "encDataLen:", encDataLen, ", EncData", return_value(EncData)

    # ----------------encrypt not used---------------end-------#

    #test decrypt
    # init dec bufer
    # decData = [0x00] * 255
    # decDataLen = ctypes.c_int(255)
    # DecData = (c_ubyte * 255)(*decData)

    file = open('./data.txt','r')
    writeFile = open('./decData.txt','wb')
    allData = ''
    lines = file.readlines()
    for line in lines:
        encData = hex2arr(line)
        encDataLen = ctypes.c_int(len(encData))
        EncData = (c_ubyte * len(encData))(*encData)

        decData = [0x00] * 255
        decDataLen = ctypes.c_int(32)
        DecData = (c_ubyte * 255)(*decData)

        # print "encDataLen:", encDataLen, ", EncData", return_value(EncData)
        status = crypto.decrypt(EncData, encDataLen, DecData, decDataLen)
        if status != 0:
            print "decrypt error"
            exit(-1)
        # print "decDataLen:", decDataLen, ", DecData", return_value(DecData)
        allData += pack_bin(DecData[0:32])
        allData += '\n'
    writeFile.write(allData)
    f = open('./decData.txt','rb')
    file_size(f, 128, 'GuoMi')
    status = crypto.closedev()
    if status != 0:
        print "close device error"
        exit(-1)
    print 'end~'