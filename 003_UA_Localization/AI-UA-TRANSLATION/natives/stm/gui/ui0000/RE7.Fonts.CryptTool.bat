@echo off
setlocal

:: 1. Шлях до утиліти (має лежати поруч із цим bat-файлом)
set "MY_TOOL=%~dp0RE7.Fonts.CryptTool.exe"

:: 2. Папка з файлами для декодування (створи папку INPUT поруч зі скриптом)
set "TARGET_FOLDER=%~dp0INPUT"

echo.
echo ==================================================
echo   МАСОВЕ ДЕКОДУВАННЯ ФАЙЛІВ
echo   Папка: %TARGET_FOLDER%
echo ==================================================
echo.

if not exist "%TARGET_FOLDER%" (
    echo [ПОМИЛКА] Не знайдено папку: %TARGET_FOLDER%
    echo Створи папку "INPUT" поруч із цим скриптом і закинь туди файли.
    pause
    exit /b
)

:: 3. Шукаємо всі файли (*) у папці
for /R "%TARGET_FOLDER%" %%F in (*) do (
    :: Ігноруємо файли, які вже мають розширення .dec, щоб не було дублів
    if /I not "%%~xF"==".dec" (
        call :DECODE "%%F"
    )
)

echo.
echo ==========================================
echo ГОТОВО! Всі файли оброблено.
echo ==========================================
pause
exit /b

:: --- ФУНКЦІЯ ДЕКОДУВАННЯ ---
:DECODE
pushd "%~dp1"

echo [ДЕКОДУВАННЯ]: %~nx1
"%MY_TOOL%" "%~nx1" "%~nx1.dec"

popd
goto :EOF