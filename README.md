# Система управления заявками жильцов

## Назначение

Консольное приложение для управления заявками жильцов многоквартирного дома:
регистрация заявок, поиск, назначение исполнителей, отслеживание статусов.

## Предметная область

Жилищно-коммунальное хозяйство (ЖКХ), сервисное обслуживание.

Основные сущности:
- **Tenant** - жилец;
- **Executor** - исполнитель (техник);
- **Request** - заявка.

## Основные классы

### Tenant — жилец

Атрибуты: `id`, `name`, `flat`, `phone`.
Методы: `from_data()`, `to_data()`, `__str__()`.

### Executor — исполнитель

Атрибуты: `id`, `name`, `specialization`, `is_busy`.
Методы: `can_handle()`, `from_data()`, `to_data()`, `__str__()`.

### Request — заявка

Атрибуты: `id`, `tenant`, `problem`, `date`, `category`, `status`, `executor`.
Методы: `assign_executor()`, `complete()`, `cancel()`,
`get_status_text()`, `from_data()`, `to_data()`, `__str__()`.

## Взаимодействие объектов

Объект `Request` связывает `Tenant` и `Executor`:
Request -> tenant -> Tenant
Request -> executor -> Executor

При назначении исполнителя `Request` устанавливает `executor.is_busy = True`.
При завершении или отмене - сбрасывает обратно в `False`.

## Хранение данных

- `data/tenants.json`
- `data/executors.json`
- `data/requests.json`

JSON хранит **идентификаторы** связанных объектов (`tenant_id`, `executor_id`).
При загрузке `storage.py` восстанавливает объектные связи.

## Запуск

```bash
pip install -r requirements.txt
python main.py
```

## Тесты

```bash
pytest -v
flake8 .
```
