# Система управления заявками жильцов - ПР7

Веб-приложение Django для просмотра жильцов, исполнителей и заявок ЖКХ.
Данные веб-страниц читаются из SQLite напрямую через стандартный модуль sqlite3,
без Django ORM. Предыдущая реализация и описание сохранены в README_PR1_PR6.md,
storage.py, models/, main.py и исходных JSON-файлах.

## Запуск (PowerShell, из корня проекта)

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m db.import_json
python manage.py check
python manage.py runserver
```

Открыть http://127.0.0.1:8000/. Импорт повторяемый: заменяет снимок данных одной
транзакцией, не создает дубликаты. Он намеренно перезаписывает SQLite данными JSON;
не запускайте его для сохранения ручных изменений в SQLite. Ошибка внешнего ключа
откатывает замену данных. Пути не зависят от текущей папки.

## Структура SQL-слоя

- `data/tenant_requests.sqlite` - база предметной области, отдельно от db.sqlite3 Django.
- `sql/schema.sql` - создание таблиц, индексов, CHECK и внешних ключей.
- `sql/queries.sql` - 13 именованных параметризованных SELECT с комментариями.
- `db/database.py` - connect(), sqlite3.Row, PRAGMA foreign_keys, закрытие соединения;
  fetch() читает запросы непосредственно из queries.sql.
- `db/import_json.py` - executemany(), параметры ?, commit(), атомарный повторный импорт.
- `tests/test_sqlite.py` - изолированная база: импорт, откат, FK, SQL, страницы и фильтры.

## Схема базы

| Таблица | Поля |
|---|---|
| tenants | id INTEGER PK, name TEXT NOT NULL, flat INTEGER NOT NULL (>0), phone TEXT NULL |
| executors | id INTEGER PK, name TEXT NOT NULL, specialization TEXT NOT NULL, is_busy INTEGER NOT NULL (0/1) |
| requests | id INTEGER PK, tenant_id INTEGER NOT NULL FK tenants(id), problem TEXT NOT NULL, date TEXT NOT NULL, category TEXT NOT NULL, status TEXT NOT NULL, executor_id INTEGER NULL FK executors(id) |

Один жилец имеет много заявок; один исполнитель имеет много заявок. У заявки
исполнитель может отсутствовать (NULL). Удаление связанных родителей запрещено
ON DELETE RESTRICT. Даты хранятся ISO YYYY-MM-DD; импорт проверяет их через date.fromisoformat.
Статусы: Новая, В работе, Выполнена, Отменена. Индексы: tenant_id, executor_id,
(category, status). Импортировано по 2 жильца, исполнителя и заявки; исходные значения
сохранены, включая заявку «В работе» без исполнителя.

## Запросы и страницы

| Именованные запросы | Тип и назначение | URL |
|---|---|---|
| tenants, executors | Два списка, ORDER BY, у жильцов LIMIT/OFFSET | /tenants/, /executors/ |
| tenant_search | WHERE, LIKE и квартира | /tenants/?q=109 |
| available_executors | WHERE, AND, NOT EXISTS: свободные по специализации | /executors/?available=1&specialization=сантехника |
| requests | JOIN жильцов, LEFT JOIN исполнителей, фильтры | /requests/?category=электрика&status=В%20работе |
| tenant_requests | JOIN: заявки конкретного жильца | /tenants/1/ |
| request_totals, executor_totals | Два агрегатных запроса COUNT/SUM/COALESCE | /requests/statistics/ |
| category_stats | GROUP BY категорий, COUNT/MIN/MAX | /requests/statistics/ |
| executor_stats | GROUP BY исполнителей, HAVING, учитывается нулевая нагрузка | /requests/statistics/?minimum=1 |
| tenant_detail, executor_detail, request_detail | Карточки объектов; для заявки JOIN | /tenants/1/, /executors/1/, /requests/1/ |

Первые 10 запросов покрывают по два запроса каждого обязательного вида. Все 13
используются Django-представлениями; значения передаются отдельно, по полям Row
обращаемся по именам. Пустые результаты показывают сообщение, неизвестный ID дает 404.
Специализация применяется при включении «Только свободные». Свободный исполнитель
имеет is_busy=0 и не имеет активных заявок (Новая / В работе). Статистика дополнительно
показывает учетный признак is_busy; это не календарь: исходная модель не содержит
интервалов занятости. Примеры Roomly из методички адаптированы к предметной области ЖКХ.

## Проверки и защита

```powershell
python manage.py check
python -m pytest -v
python -m flake8 . --extend-exclude=venv
sqlite3 data/tenant_requests.sqlite ".schema"
sqlite3 data/tenant_requests.sqlite "PRAGMA integrity_check; PRAGMA foreign_key_check;"
```

Для запроса из queries.sql в SQLite CLI предварительно задайте параметры:
`.parameter init`, `.parameter set ?1 20`, `.parameter set ?2 0`, затем выполните
SELECT списка жильцов. Пользовательские значения не подставляются в SQL-строки.
В ограниченной среде для pytest можно указать --basetemp с доступной папкой.

Результаты ПР7: manage.py check - ошибок нет; pytest - 17 passed; flake8 - замечаний
нет. Проверены все 13 запросов через SQLite CLI. integrity_check: ok,
foreign_key_check: пусто. Ветка pr7-sqlite; коммиты работы начинаются с PR7:.
Факт прохождения курса Яндекс Практикума и установка расширения VS Code не подтверждены.
