@echo off
cd /d %~dp0
python\python.exe src\main.py -i %1 -m csv
pause
