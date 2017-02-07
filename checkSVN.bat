
@ECHO OFF

:RETRY
REM C:\CygWin64\bin\wget.exe http://OyewoleL:affinity123@sunsoasvc01.grpdom.vwuk.corp/SOA/ > C:\tmp\wget.out
C:\CygWin64\bin\wget.exe http://OyewoleL:affinity123@sunsoasvc01.grpdom.vwuk.corp/SOA/ -o C:\tmp\wgetSVN.out

findstr 200 C:\tmp\wgetSVN.out > NUL
IF ERRORLEVEL 1 GOTO WAIT-A-MINUTE
GOTO FINISH

:WAIT-A-MINUTE
REM C:\windows\system32\timeout /t 60
ping 1.1.1.1 -n 1 -w 60000 > NUL
GOTO RETRY

:FINISH
