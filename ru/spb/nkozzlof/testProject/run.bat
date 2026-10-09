@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

cd /d "%~dp0"

REM --- Пути к подпапкам ---
set APP_DIR=%~dp0app
set DB_DIR=%~dp0db
set SQL_FILE=%DB_DIR%\createDb.sql

echo ============================================
echo   Запуск приложения учёта заказов
echo ============================================
echo [i] APP_DIR : %APP_DIR%
echo [i] SQL_FILE: %SQL_FILE%
echo.

REM --- Проверка Python ---
where python >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден в PATH.
    echo Запустите setup.bat или установите Python 3.10+.
    pause
    exit /b 1
)

REM --- Проверка venv ---
if not exist ".venv\Scripts\activate.bat" (
    echo [!] Виртуальное окружение .venv не найдено.
    echo     Запускаю setup.bat ...
    echo.
    call setup.bat
    if errorlevel 1 exit /b 1
)

REM --- Активация venv ---
call .venv\Scripts\activate.bat

REM --- Проверка psycopg2 ---
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo [!] Модуль psycopg2 не установлен. Устанавливаю...
    pip install -r "%APP_DIR%\requirements.txt"
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось установить зависимости.
        pause
        exit /b 1
    )
)

REM --- Параметры подключения (можно переопределить снаружи) ---
if not defined PGHOST     set PGHOST=localhost
if not defined PGPORT     set PGPORT=5432
if not defined PGDATABASE set PGDATABASE=orders_db
if not defined PGUSER     set PGUSER=orders_user
if not defined PGPASSWORD set PGPASSWORD=orders_pass

echo [i] PostgreSQL: %PGUSER%@%PGHOST%:%PGPORT%/%PGDATABASE%
echo.

REM --- Проверка подключения к БД ---
python -c "import psycopg2, os; psycopg2.connect(host=os.environ['PGHOST'], port=os.environ['PGPORT'], dbname=os.environ['PGDATABASE'], user=os.environ['PGUSER'], password=os.environ['PGPASSWORD']).close()" >nul 2>&1
if errorlevel 1 (
    echo [!] Не удалось подключиться к БД.
    echo     Проверьте, что PostgreSQL запущен и параметры в app\config.py верны.
    echo.
    set /p ANS="Выполнить инициализацию БД (init_db.bat)? [y/N]: "
    if /i "!ANS!"=="y" (
        call init_db.bat
        if errorlevel 1 (
            echo [ОШИБКА] Инициализация БД не удалась.
            pause
            exit /b 1
        )
    ) else (
        echo Выход.
        pause
        exit /b 1
    )
) else (
    echo [OK] Подключение к БД успешно.
)
echo.

REM --- Переход в app\ и запуск приложения ---
pushd "%APP_DIR%"
echo [*] Рабочий каталог: %CD%
echo [*] Запускаю app.py ...
echo --------------------------------------------
python app.py
set EXITCODE=%ERRORLEVEL%
echo --------------------------------------------
popd

if %EXITCODE% neq 0 (
    echo.
    echo [ОШИБКА] Приложение завершилось с кодом %EXITCODE%.
    pause
) else (
    echo.
    echo [OK] Приложение закрыто штатно.
)

endlocal