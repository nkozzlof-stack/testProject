import psycopg2
from config import DB_CONFIG


def get_connection():
    """Новое соединение с БД (search_path=test_orders)."""
    return psycopg2.connect(**DB_CONFIG)


# ==================== Клиенты ====================
def get_clients():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT c_id, c_fio
            FROM test_orders.clients
            ORDER BY c_fio
        """)
        return cur.fetchall()


def add_client(fio: str):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO test_orders.clients (c_fio)
            VALUES (%s) RETURNING c_id
        """, (fio,))
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id


def update_client(c_id: int, fio: str):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            UPDATE test_orders.clients
               SET c_fio=%s
             WHERE c_id=%s
        """, (fio, c_id))
        conn.commit()


def delete_client(c_id: int):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM test_orders.clients WHERE c_id=%s", (c_id,))
        conn.commit()


# ==================== Артикулы ====================
def get_articles():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT a_id, a_name
            FROM test_orders.order_groups
            ORDER BY a_name
        """)
        return cur.fetchall()


# ==================== Заказы ====================
def get_orders():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT o.o_id, o.datetime, c.c_fio, g.a_name
            FROM test_orders.orders       o
            JOIN test_orders.clients      c ON c.c_id = o.o_client_id
            JOIN test_orders.order_groups g ON g.a_id = o.group_id
            ORDER BY o.datetime DESC
        """)
        return cur.fetchall()


def add_order(dt, client_id: int, group_id: int):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO test_orders.orders (datetime, o_client_id, group_id)
            VALUES (%s, %s, %s) RETURNING o_id
        """, (dt, client_id, group_id))
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id


def update_order(o_id: int, dt, client_id: int, group_id: int):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            UPDATE test_orders.orders
               SET datetime=%s, o_client_id=%s, group_id=%s
             WHERE o_id=%s
        """, (dt, client_id, group_id, o_id))
        conn.commit()


def delete_order(o_id: int):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM test_orders.orders WHERE o_id=%s", (o_id,))
        conn.commit()


# ==================== Отчёты ====================
def report_orders_by_client():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT c.c_id, c.c_fio, COUNT(o.o_id) AS orders_count
            FROM test_orders.clients c
            LEFT JOIN test_orders.orders o ON o.o_client_id = c.c_id
            GROUP BY c.c_id, c.c_fio
            ORDER BY orders_count DESC, c.c_fio
        """)
        return cur.fetchall()


def report_orders_last_month():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT o.o_id, o.datetime, c.c_fio, g.a_name
            FROM test_orders.orders       o
            JOIN test_orders.clients      c ON c.c_id = o.o_client_id
            JOIN test_orders.order_groups g ON g.a_id = o.group_id
            WHERE o.datetime >= NOW() - INTERVAL '1 month'
            ORDER BY o.datetime DESC
        """)
        return cur.fetchall()


def report_orders_by_article():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT g.a_id, g.a_name, COUNT(o.o_id) AS orders_count
            FROM test_orders.order_groups g
            LEFT JOIN test_orders.orders o ON o.group_id = g.a_id
            GROUP BY g.a_id, g.a_name
            ORDER BY orders_count DESC, g.a_name
        """)
        return cur.fetchall()