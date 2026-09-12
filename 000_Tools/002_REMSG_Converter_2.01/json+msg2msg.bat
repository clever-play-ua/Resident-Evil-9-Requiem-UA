@echo off
cd /d %~dp0
python\python.exe src\main.py -m json %1 %2
pause
