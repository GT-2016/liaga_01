@echo off
set /p ip="input ip:"
echo set sh=WScript.CreateObject("WScript.Shell") >telnet_tmp.vbs

echo WScript.Sleep 2000 >>telnet_tmp.vbs
rem ----------------UNIX IPAddress
echo sh.SendKeys "open %ip% 2301{ENTER}" >>telnet_tmp.vbs

echo WScript.Sleep 2000 >>telnet_tmp.vbs
rem ----------------password
echo sh.SendKeys "qtec{ENTER}" >>telnet_tmp.vbs

echo WScript.Sleep 2000 >>telnet_tmp.vbs
rem ----------------en
echo sh.SendKeys "en {ENTER}" >>telnet_tmp.vbs
rem ----------------con te
echo WScript.Sleep 2000 >>telnet_tmp.vbs
echo sh.SendKeys "con te {ENTER}">>telnet_tmp.vbs
rem ----------------snmp
echo WScript.Sleep 1000 >>telnet_tmp.vbs
echo sh.SendKeys "snmp {ENTER}">>telnet_tmp.vbs
rem ----------------community----------------
echo WScript.Sleep 1000 >>telnet_tmp.vbs
echo sh.SendKeys "rwcommunity public {ENTER}">>telnet_tmp.vbs
echo WScript.Sleep 1000 >>telnet_tmp.vbs
echo sh.SendKeys "trap 10.64.102.242 162 public {ENTER}">>telnet_tmp.vbs
echo WScript.Sleep 1000 >>telnet_tmp.vbs
echo sh.SendKeys "cpu 89 {ENTER}">>telnet_tmp.vbs
echo WScript.Sleep 1000 >>telnet_tmp.vbs
echo sh.SendKeys "disk 85 {ENTER}">>telnet_tmp.vbs
echo WScript.Sleep 1000 >>telnet_tmp.vbs
echo sh.SendKeys "write {ENTER}">>telnet_tmp.vbs
echo WScript.Sleep 1000 >>telnet_tmp.vbs
echo sh.SendKeys "q {ENTER}">>telnet_tmp.vbs
echo WScript.Sleep 1000 >>telnet_tmp.vbs
echo sh.SendKeys "q {ENTER}">>telnet_tmp.vbs
echo WScript.Sleep 1000 >>telnet_tmp.vbs
echo sh.SendKeys "q {ENTER}">>telnet_tmp.vbs

start telnet %ip% 2301

cscript //nologo telnet_tmp.vbs

del telnet_tmp.vbs