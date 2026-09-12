@echo off
pyinstaller --onefile --noconsole --name "REE.Fonts.Cryptor" --icon REE_Fonts_Cryptor.ico REE_Fonts_Cryptor.py
echo.
echo Build เสร็จแล้ว! ไฟล์อยู่ที่โฟลเดอร์ dist
explorer dist
pause
