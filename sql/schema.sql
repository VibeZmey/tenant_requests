PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS tenants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK(length(trim(name)) > 0),
    flat INTEGER NOT NULL CHECK(flat > 0),
    phone TEXT
);
CREATE TABLE IF NOT EXISTS executors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    is_busy INTEGER NOT NULL DEFAULT 0 CHECK(is_busy IN (0, 1))
);
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    problem TEXT NOT NULL,
    date TEXT NOT NULL CHECK(date GLOB '????-??-??'),
    category TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Новая','В работе','Выполнена','Отменена')),
    executor_id INTEGER REFERENCES executors(id) ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_requests_tenant ON requests(tenant_id);
CREATE INDEX IF NOT EXISTS idx_requests_executor ON requests(executor_id);
CREATE INDEX IF NOT EXISTS idx_requests_category_status ON requests(category, status);
