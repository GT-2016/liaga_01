#-*-coding:utf-8-*-
import time,sys
import random,string
from pykeyboard import *
from pymouse import *
import win32file
import itertools
list_pass = list(string.digits + string.ascii_letters)
list_digits = list(string.digits)
list_letters=list(string.ascii_letters)

passwd = '1234567a'
new_passwd = '123456'
conform_new_passwd = '123456'
# 所有的坐标均为相对坐标
# for i in itertools.permutations('abcd',2):
#     print ''.join(i)
# for i in itertools.product(*[a] * b):
#     print ''.join(i)
m = PyMouse()
k = PyKeyboard()
time.sleep(1)
print m.position()
# --------------------管理员用户名+密码不停登录----start------------------#
# m.click(370, 550)   #admin
# k.type_string('admin')
# m.click(370,610)    #password
# #组合6-18位数字、字母组合
# try:
#     for js in range(6,7):
#         for i in itertools.product(*[list_pass] * js):
#               
#             time.sleep(1)
#             str_passwd = ''.join(i)
#             m.click(370,610)    #password
#             k.type_string(str_passwd)
#             m.click(370,675)    #登1
#             print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'str_passwd: ',str_passwd
#             time.sleep(0.5)
#             m.click(941,520)    #确认
#             time.sleep(0.5)
#             m.click(370,610)    #密码
# #             m.click(370,610)
#             k.tap_key(k.end_key)
#             time.sleep(0.5)
#             for gt in range(js):
#                 k.tap_key(k.backspace_key)
# #             print 'i',js
# #             break
#     print time.time()
# except KeyboardInterrupt:
#     print 'ctrl + c'
# --------------------管理员用户名+密码不停登录----end------------------#
# k.release_key(k.shift_key)
# k.tap_key(k.backspace_key)      
# k.type_string
# 移动到需要操作的按钮上12
#键盘在input框中输入内容
#----------------------模拟修改密码的功能-start---------------------#
# x2,y2 = m.position()
# print x2,y2 
# m.click(x2, y2)
# k.type_string(passwd)       #raw_input('新密码')
# k.tap_key(k.tab_key)
# k.type_string(new_passwd)
# k.tap_key(k.tab_key)
# k.type_string(conform_new_passwd)
# m.click(x2, y2+200)
#----------------------模拟修改密码的功能-end---------------------#
# 检测到鼠标变化后，可以实时输入鼠标坐标

# -------------不停注入密钥--start--------------------#
def insertKey(num):
    for i in range(num):
    #     print 'i:',i     
        m.click(680, 570)
        time.sleep(0.5)
        m.click(950,528)
        time.sleep(0.5)
# ------------不停签发新Q盾--start--------------------#
def registerQKey(num):
    for i in range(num):
    #     print 'i:',i     
        m.click(256, 397)
        time.sleep(0.5)
        m.click(957,522)
        time.sleep(0.5)

def clickPosition(num):
    for i in range(num):
        m.click(708,674)
        time.sleep(1)      
# try:
#     insertKey(50)
# except BaseException as e:
#     print e.message
#     sys.exit()
# -------------不停注入密钥--end--------------------#
if __name__ == '__main__':
#     clickPosition(150)
#     registerQKey(10)
    insertKey(500)
    print 'main'
    