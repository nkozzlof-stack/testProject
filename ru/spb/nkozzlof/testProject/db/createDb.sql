-- ============================================================
-- Схема test_orders для приложения учёта заказов (PostgreSQL)
-- ============================================================

-- Создать схему (если её ещё нет)
CREATE SCHEMA IF NOT EXISTS test_orders;

-- Удаление таблиц (для повторного применения)
DROP TABLE IF EXISTS test_orders.orders        CASCADE;
DROP TABLE IF EXISTS test_orders.order_groups  CASCADE;
DROP TABLE IF EXISTS test_orders.clients       CASCADE;

-- ---------- Клиенты ----------
CREATE TABLE test_orders.clients (
    c_id    SERIAL PRIMARY KEY,
    c_fio   VARCHAR(200) NOT NULL
);

-- ---------- Артикулы ----------
CREATE TABLE test_orders.order_groups (
    a_id    SERIAL PRIMARY KEY,
    a_name  VARCHAR(200) NOT NULL UNIQUE
);

-- ---------- Заказы ----------
CREATE TABLE test_orders.orders (
    o_id         SERIAL PRIMARY KEY,
    datetime     TIMESTAMP NOT NULL DEFAULT NOW(),
    o_client_id  INTEGER NOT NULL,
    group_id     INTEGER NOT NULL,
    CONSTRAINT fk_orders_client
        FOREIGN KEY (o_client_id) REFERENCES test_orders.clients(c_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_orders_group
        FOREIGN KEY (group_id) REFERENCES test_orders.order_groups(a_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Индексы для ускорения отчётов
CREATE INDEX idx_orders_client ON test_orders.orders(o_client_id);
CREATE INDEX idx_orders_group  ON test_orders.orders(group_id);
CREATE INDEX idx_orders_dt     ON test_orders.orders(datetime);

-- ---------- Заполнение артикулов (5 позиций) ----------
INSERT INTO test_orders.order_groups (a_name) VALUES
    ('Ноутбук Lenovo IdeaPad'),
    ('Смартфон Samsung Galaxy'),
    ('Планшет iPad Air'),
    ('Монитор Dell 24"'),
    ('Клавиатура Logitech K380')
ON CONFLICT (a_name) DO NOTHING;