@echo off
cd /d %~dp0
python\python.exe src\main.py -m csv %1 %2
pause
