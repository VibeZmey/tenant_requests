-- name: tenants
-- Список жильцов, сортировка и пагинация
SELECT * FROM tenants ORDER BY flat, id LIMIT ? OFFSET ?;

-- name: executors
-- Список исполнителей
SELECT * FROM executors ORDER BY name, id;

-- name: tenant_search
-- WHERE: поиск жильцов по имени или квартире
SELECT * FROM tenants WHERE name LIKE ? OR CAST(flat AS TEXT) = ? ORDER BY flat, id;

-- name: available_executors
-- WHERE: свободные исполнители выбранной специализации
SELECT * FROM executors e WHERE is_busy = 0 AND (? = '' OR specialization = ?) AND NOT EXISTS (SELECT 1 FROM requests r WHERE r.executor_id = e.id AND r.status IN ('Новая','В работе')) ORDER BY name, id;

-- name: requests
-- JOIN: заявки с жильцами и исполнителями
SELECT r.*, t.name AS tenant_name, t.flat, e.name AS executor_name
FROM requests r JOIN tenants t ON t.id = r.tenant_id
LEFT JOIN executors e ON e.id = r.executor_id
WHERE (? = '' OR r.category = ?) AND (? = '' OR r.status = ?)
ORDER BY r.date DESC, r.id DESC;

-- name: tenant_requests
-- JOIN: заявки выбранного жильца
SELECT r.*, t.name AS tenant_name, t.flat, e.name AS executor_name
FROM tenants t JOIN requests r ON r.tenant_id = t.id
LEFT JOIN executors e ON e.id = r.executor_id
WHERE t.id = ? ORDER BY r.date DESC, r.id DESC;

-- name: request_totals
-- Агрегаты: количество, выполненные и неназначенные заявки
SELECT COUNT(*) AS total,
COALESCE(SUM(CASE WHEN status = 'Выполнена' THEN 1 ELSE 0 END), 0) AS done,
COALESCE(SUM(CASE WHEN executor_id IS NULL THEN 1 ELSE 0 END), 0) AS unassigned
FROM requests;

-- name: executor_totals
-- Агрегаты: всего исполнителей и свободных по учетному признаку
SELECT COUNT(*) AS total, COALESCE(SUM(is_busy), 0) AS busy,
COALESCE(SUM(1 - is_busy), 0) AS free FROM executors;

-- name: category_stats
-- GROUP BY: количество и диапазон дат по категориям
SELECT category, COUNT(*) AS total, MIN(date) AS first_date, MAX(date) AS last_date
FROM requests GROUP BY category ORDER BY total DESC, category;

-- name: executor_stats
-- GROUP BY, HAVING: нагрузка исполнителей, включая нулевую
SELECT e.id, e.name, COUNT(r.id) AS total,
COALESCE(SUM(CASE WHEN r.status IN ('Новая','В работе') THEN 1 ELSE 0 END), 0) AS active
FROM executors e LEFT JOIN requests r ON r.executor_id = e.id
GROUP BY e.id, e.name HAVING COUNT(r.id) >= ? ORDER BY total DESC, e.id;

-- name: tenant_detail
-- Карточка жильца
SELECT * FROM tenants WHERE id = ?;

-- name: executor_detail
-- Карточка исполнителя
SELECT * FROM executors WHERE id = ?;

-- name: request_detail
-- Карточка заявки со связанными данными
SELECT r.*, t.name AS tenant_name, t.flat, e.name AS executor_name
FROM requests r JOIN tenants t ON t.id = r.tenant_id
LEFT JOIN executors e ON e.id = r.executor_id WHERE r.id = ?;
