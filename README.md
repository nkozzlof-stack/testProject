# OrderApp — учёт заказов

Десктопное приложение на Python + Tkinter + PostgreSQL для ведения клиентов и заказов.

## Возможности

- Справочник клиентов (добавление / редактирование / удаление)
- Оформление заказов с выбором клиента, артикула и даты
- Три встроенных отчёта:
  1. Количество заказов по каждому клиенту
  2. Заказы за последний месяц с ФИО и артикулом
  3. Количество заказов по артикулам

## Структура проекта
testProject/
├── app/ # исходный код
│ ├── app.py # GUI (Tkinter)
│ ├── db.py # слой работы с PostgreSQL
│ ├── init_db.py # создание схемы БД
│ ├── config.py # параметры подключения
│ └── requirements.txt
├── db/
│ └── createDb.sql # DDL: схема test_orders + 5 артикулов
├── setup.bat # разовая установка окружения
├── init_db.bat # создание схемы test_orders
├── run.bat # запуск приложения
└── build.bat # сборка OrderApp.exe (PyInstaller)
Установить окружение:
setup.bat

Создать схему test_orders:
init_db.bat

Запустить приложение:
run.bat

Сборка EXE
build.bat
Результат: dist\OrderApp.exe.

Настройка
Параметры подключения к БД — в app/config.py (DB_CONFIG).
Их также можно переопределить переменными окружения: PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD.
