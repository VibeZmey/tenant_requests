# Система управления заявками жильцов

## Назначение

Приложение для управления заявками жильцов многоквартирного дома: регистрация заявок, поиск, назначение исполнителей, отслеживание статусов. 
В ходе выполнения ПР5 проект переведён из консольного формата в веб-приложение на фреймворке Django.

## Предметная область

Жилищно-коммунальное хозяйство (ЖКХ), сервисное обслуживание.

Основные сущности:
- **Tenant** — жилец;
- **Executor** — исполнитель (техник);
- **Request** — заявка.

## Используемые технологии

- Python 3;
- Django 5.2 — веб-фреймворк;
- HTML, CSS, Bootstrap 5.3 — оформление веб-страниц;
- JSON — хранение данных;
- pytest — автоматизированные тесты;
- flake8 — проверка качества кода.

## Основные классы (ПР3)

### Tenant — жилец
Атрибуты: `id`, `name`, `flat`, `phone`.
Методы: `from_data()`, `to_data()`, `__str__()`.

### Executor — исполнитель
Атрибуты: `id`, `name`, `specialization`, `is_busy`.
Методы: `can_handle()`, `from_data()`, `to_data()`, `__str__()`.

### Request — заявка
Атрибуты: `id`, `tenant`, `problem`, `date`, `category`, `status`, `executor`.
Методы: `assign_executor()`, `complete()`, `cancel()`, `get_status_text()`, `from_data()`, `to_data()`, `__str__()`.

## Взаимодействие объектов

Объект `Request` связывает `Tenant` и `Executor`:
Request -> tenant -> Tenant
Request -> executor -> Executor


При назначении исполнителя `Request` устанавливает `executor.is_busy = True`.
При завершении или отмене — сбрасывает обратно в `False`.

## Веб-интерфейс (ПР5)

Веб-часть реализована с помощью Django. Созданы 4 приложения:
- `homepage` — главная страница, навигация и общий каркас (функция `page()`);
- `tenants` — страницы жильцов;
- `executors` — страницы исполнителей;
- `requests` — страницы заявок.

### Реализованные страницы и URL

| Страница | URL | View-функция | Описание |
|---|---|---|---|
| Главная | `/` | `homepage.views.index` | Описание приложения, кнопки перехода |
| Жильцы | `/tenants/` | `tenants.views.tenant_list` | Список всех жильцов из JSON |
| Жилец | `/tenants/<int:tenant_id>/` | `tenants.views.tenant_detail` | Карточка жильца (или 404) |
| Исполнители | `/executors/` | `executors.views.executor_list` | Список всех исполнителей |
| Исполнитель | `/executors/<int:executor_id>/`| `executors.views.executor_detail` | Карточка исполнителя (или 404) |
| Заявки | `/requests/` | `requests.views.request_list` | Список всех заявок со статусами |
| Заявка | `/requests/<int:request_id>/` | `requests.views.request_detail` | Карточка заявки (или 404) |

При отсутствии объекта с указанным ID возвращается HTTP-статус 404 и соответствующая страница. Настроен кастомный обработчик ошибки 404 (`handler404`).

## Хранение данных

На текущем этапе данные хранятся в JSON-файлах:
- `data/tenants.json`
- `data/executors.json`
- `data/requests.json`

JSON хранит **идентификаторы** связанных объектов (`tenant_id`, `executor_id`).
При загрузке `storage.py` восстанавливает объектные связи, а веб-слой (view-функции) использует готовые объекты классов ПР3 для формирования HTML.

## Структура проекта

```text
tenant_requests/
├── .flake8
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py                 # Управление Django (ПР5)
├── main.py                   # Консольный запуск (ПР3)
├── storage.py                # Загрузка/сохранение JSON
├── utils.py                  # Безопасный ввод
├── tenant_requests/          # Настройки Django-проекта
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── homepage/                 # Приложение: главная
│   ├── views.py
│   └── urls.py
├── tenants/                  # Приложение: жильцы
│   ├── views.py
│   └── urls.py
├── executors/                # Приложение: исполнители
│   ├── views.py
│   └── urls.py
├── requests/                 # Приложение: заявки
│   ├── views.py
│   └── urls.py
├── models/                   # Классы предметной области (ПР3)
│   ├── __init__.py
│   ├── tenants.py
│   ├── executors.py
│   └── requests.py
├── data/                     # JSON-файлы данных
│   ├── tenants.json
│   ├── executors.json
│   └── requests.json
└── tests/                    # Тесты (ПР2-ПР3)
    ├── test_tenants.py
    ├── test_executors.py
    └── test_requests.py