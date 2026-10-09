import os

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "postgres",
    "user":     "postgres",
    "password": "postgres",
    "options":  "-c search_path=test_orders,public",
}

# app/  →  на уровень выше  →  db/createDb.sql
APP_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)          # .../testProject
SQL_SCHEMA_PATH = os.path.join(PROJECT_ROOT, "db", "createDb.sql")

# Можно переопределить через переменную окружения
SQL_SCHEMA_PATH = os.environ.get("ORDERS_SQL_PATH", SQL_SCHEMA_PATH)