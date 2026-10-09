@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM --- Переход в каталог, где лежит сам bat ---
cd /d "%~dp0"

echo ============================================
echo   Установка окружения проекта
echo ============================================
echo.

REM --- Проверка Python ---
where python >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден в PATH.
    echo Установите Python 3.10+ с https://www.python.org/downloads/
    echo При установке отметьте "Add Python to PATH".
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% найден.
echo.

REM --- Проверка структуры ---
if not exist "app\app.py" (
    echo [ОШИБКА] Не найден app\app.py
    echo Проверьте структуру проекта.
    pause
    exit /b 1
)
if not exist "db\createDb.sql" (
    echo [!] Предупреждение: db\createDb.sql не найден.
)

REM --- Создание venv ---
if not exist ".venv" (
    echo [*] Создаю виртуальное окружение .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось создать .venv
        pause
        exit /b 1
    )
    echo [OK] .venv создано.
) else (
    echo [OK] .venv уже существует.
)
echo.

REM --- Активация и установка зависимостей ---
call .venv\Scripts\activate.bat

echo [*] Обновляю pip ...
python -m pip install --upgrade pip >nul

if exist "app\requirements.txt" (
    echo [*] Устанавливаю зависимости из app\requirements.txt ...
    pip install -r "app\requirements.txt"
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось установить зависимости.
        pause
        exit /b 1
    )
    echo [OK] Зависимости установлены.
) else (
    echo [!] app\requirements.txt не найден — пропускаю.
)
echo.

echo ============================================
echo   Готово! Теперь запустите run.bat
echo ============================================
pause
endlocal