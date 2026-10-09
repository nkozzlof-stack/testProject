"""
Создаёт схему test_orders и таблицы.
SQL-скрипт берётся из config.SQL_SCHEMA_PATH.
Запуск:  python init_db.py
"""
import os
import sys
import argparse
import psycopg2

from config import DB_CONFIG, SQL_SCHEMA_PATH


def load_sql(path: str) -> str:
    if not os.path.isfile(path):
        sys.exit(f"❌ SQL-файл не найден: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Инициализация схемы test_orders")
    parser.add_argument(
        "--sql", "-s",
        default=SQL_SCHEMA_PATH,
        help="Путь к SQL-файлу (по умолчанию берётся из config.SQL_SCHEMA_PATH)"
    )
    args = parser.parse_args()

    sql_path = os.path.abspath(args.sql)
    print(f"📄 Используется SQL-файл: {sql_path}")
    ddl = load_sql(sql_path)

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute(ddl)
        print("✅ Схема test_orders успешно создана и заполнена.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()