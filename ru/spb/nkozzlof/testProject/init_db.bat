@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

cd /d "%~dp0"

set APP_DIR=%~dp0app
set SQL_FILE=%~dp0db\createDb.sql

echo ============================================
echo   Инициализация БД (схема test_orders)
echo ============================================
echo [i] APP_DIR : %APP_DIR%
echo [i] SQL_FILE: %SQL_FILE%
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo [ОШИБКА] Нет .venv. Сначала запустите setup.bat
    pause
    exit /b 1
)

if not exist "%SQL_FILE%" (
    echo [ОШИБКА] SQL-файл не найден: %SQL_FILE%
    pause
    exit /b 1
)

if not exist "%APP_DIR%\init_db.py" (
    echo [ОШИБКА] Не найден %APP_DIR%\init_db.py
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

echo [*] Запускаю init_db.py ...
echo --------------------------------------------
pushd "%APP_DIR%"
python init_db.py --sql "%SQL_FILE%"
set EXITCODE=%ERRORLEVEL%
popd
echo --------------------------------------------

if %EXITCODE% neq 0 (
    echo.
    echo [ОШИБКА] Инициализация БД завершилась с ошибкой.
    pause
    exit /b 1
)

echo.
echo [OK] БД успешно инициализирована.
pause
endlocal