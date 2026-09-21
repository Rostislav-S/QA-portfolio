# Python API — Автотесты для TotalShiftLeft REST API

> Автотесты на Python для публичного sandbox-API TotalShiftLeft. Переносят сценарии из Postman-коллекции в pytest-тесты: от smoke-проверок до негативных сценариев и глубокой валидации схем.

## 📂 Содержимое

| Файл / директория | Назначение |
|:---|:---|
| [`tests/`](./tests/) | Пять модулей тестов: smoke, CRUD, query-параметры, ошибки, продвинутая валидация |
| [`schemas/`](./schemas/) | JSON-схемы для валидации ответов (user, pagination, error) |
| [`helpers/`](./helpers/) | Генерация уникальных тестовых данных |
| [`conftest.py`](./conftest.py) | Фикстуры: `api_client`, `created_user`, `unique_user` |
| [`pytest.ini`](./pytest.ini) | Конфигурация pytest и маркеры |
| [`requirements.txt`](./requirements.txt) | Зависимости проекта |
| [`.env.example`](./.env.example) | Шаблон переменных окружения |

## 🧰 Стек

| Библиотека | Назначение |
|:---|:---|
| **pytest** | Фреймворк для тестов |
| **requests** | HTTP-клиент |
| **jsonschema** | Валидация структуры JSON-ответов |
| **python-dotenv** | Загрузка переменных окружения из `.env` |
| **pytest-html** | Генерация HTML-отчёта о прогоне |

## 🚀 Как запускать

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Rostislav-S/QA-portfolio.git
cd QA-portfolio/python_api
```
### 2. Создать виртуальное окружение

```bash
# Windows
python -m venv venv
venv\Scripts\activate
# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```


### 4. Настроить `.env`

```bash
cp .env.example .env
```

Значения по умолчанию подходят для запуска без изменений.

### 5. Запустить тесты

```
bash

# Все тесты
pytest
# Только smoke
pytest -m smoke
# Только CRUD
pytest -m crud
# Только негативные
pytest -m error
# С подробным выводом
pytest -v
# С генерацией HTML-отчёта
pytest --html=reports/report.html --self-contained-html
```

После прогона HTML-отчёт появится в `reports/report.html`.

## 📁 Структура проекта

```text

python_api/
│
├── conftest.py                    # Фикстуры (api_client, created_user, base_url)
├── pytest.ini                     # Конфигурация pytest
├── requirements.txt               # Зависимости
├── .env.example                   # Шаблон переменных окружения
├── .gitignore
├── README.ru.md                   # Этот файл
│
├── tests/
│   ├── test_01_smoke.py           # Smoke-проверки доступности
│   ├── test_02_crud_users.py      # CRUD-операции над users
│   ├── test_03_query_filtering.py # Query-параметры: фильтрация, пагинация
│   ├── test_04_error_handling.py  # Негативные сценарии
│   └── test_05_advanced.py        # Глубокая валидация схем
│
├── schemas/
│   ├── __init__.py
│   ├── user.py                    # Схемы users
│   ├── pagination.py              # Схема блока pagination
│   └── error.py                   # Схемы ошибок (Fastify, generic)
│
├── helpers/
│   ├── __init__.py
│   └── data.py                    # Генерация уникальных тестовых данных
│
└── reports/                       # HTML-отчёты (в .gitignore)
```

## 📊 Покрытие

### 01 — Smoke (2 теста)

Базовая проверка доступности ключевых эндпоинтов. Если падают — остальные тесты не имеют смысла.

- `test_users_health_check` — `GET /users`
- `test_products_health_check` — `GET /products`

### 02 — CRUD users (4 теста)

Полный цикл CRUD над ресурсом `users`.

- `test_create_user` — `POST /users` → 201
- `test_read_user` — `GET /users/{id}` → 200
- `test_update_user` — `PATCH /users/{id}` → 200
- `test_delete_user` — `DELETE /users/{id}` → 204

**Особенность:** используется фикстура `created_user` — она создаёт пользователя до теста и удаляет после.

### 03 — Query-параметры (2 теста)

- `test_products_filter_by_category` — фильтрация по `category`
- `test_products_pagination` — пагинация через `page` и `limit`

### 04 — Негативные сценарии (5 тестов)

- `test_server_error_500` — симуляция серверной ошибки (`?error=500`)
- `test_timeout_behavior` — задержка ответа (`?delay=2000`)
- `test_invalid_uuid_format` — невалидный формат UUID в path
- `test_not_found` — несуществующий ресурс (404)
- `test_order_invalid_product_id` — невалидный `product_id` в теле (400)

### 05 — Advanced (1 тест)

- `test_users_deep_schema_validation` — глубокая валидация схемы: форматы UUID, email, ISO 8601, enum ролей, уникальность ID.

**Итого:** 14 тестов.

## 🧠 Технические приёмы

### Fixtures

- **`api_client`** — `requests.Session` с общими заголовками и базовым URL. Создаётся один раз за прогон.
- **`created_user`** — создаёт и удаляет пользователя (setup / teardown через `yield`).
- **`unique_user`** — генерация уникальных `name` и `email` через `time.time()`.

### Schema validation

Все проверки структуры ответа — через `jsonschema.validate()`. Схемы хранятся отдельно в `schemas/` и переиспользуются между тестами.

### Markers

Тесты размечены маркерами `smoke`, `crud`, `query`, `error`, `advanced`. Позволяет запускать подмножества:

```bash
pytest -m error
pytest -m "crud or smoke"
```

## 🔗 Связанные проекты

Проект синхронизирован с [Postman-коллекцией](https://../postman/) `TotalShiftLeft REST API — QA Portfolio`. Структура совпадает 1:1:

|Postman|Python|
|---|---|
|`01_Smoke`|`tests/test_01_smoke.py`|
|`02_CRUD_Users`|`tests/test_02_crud_users.py`|
|`03_Query_Filtering`|`tests/test_03_query_filtering.py`|
|`04_Error_Handling`|`tests/test_04_error_handling.py`|
|`05_Advanced_Scripts`|`tests/test_05_advanced.py`|

Оба портфолио демонстрируют разные грани одного и того же навыка: Postman — ручное исследование и скрипты, Python — автоматизацию.

## ⚠️ Ограничения sandbox

### Отсутствие продуктов

`GET /products` возвращает пустой массив — в sandbox нет продуктов. Это влияет на:

- `test_products_filter_by_category` — проверка проходит на пустом массиве.
- `test_order_invalid_product_id` — используем фиктивный UUID `"not-a-uuid"`, чтобы проверить формат.

### Валидация тела запроса

`POST /orders` использует Fastify-валидацию, которая проверяет формат `product_id` раньше, чем существование ресурса. Поэтому невалидный формат даёт 400, а не 404.

### Порядок проверок в API

Sandbox проверяет входные данные в определённом порядке:

1. Синтаксис JSON — невалидный JSON → 400.
2. Формат полей — невалидный UUID → 400 (FST_ERR_VALIDATION).
3. Существование ресурса — 404.
4. Бизнес-логика — зависит от эндпоинта.

Это важно учитывать при написании негативных тестов: ожидаемый статус-код зависит от того, на каком уровне срабатывает проверка.

## 📖 История отладки

### Ложное ожидание 403 на `POST /orders`

Первоначально запрос `POST /orders` считался защищённым эндпоинтом, и в тестах ожидался ответ `403 Forbidden`. Причины расхождений между клиентами:

1. В Postman использовался метод `GET` вместо `POST` (случайная опечатка) — сервер возвращал 403 или 404.
2. В теле `user_id` был без кавычек — невалидный JSON, ошибка `Unexpected token f in JSON at position 19` → 400.
3. В Python `product_id` передавался как число — Fastify-валидация отклоняла запрос → 400.

После исправления всех трёх ошибок запрос вернул `201 Created` во всех клиентах: Postman, curl, Python `requests`.

Вывод: негативные тесты пишутся только после ручной проверки реального поведения эндпоинта. Ожидание «на глаз» приводит к ложным падениям и путанице.

### Правило кавычек в JSON

При подстановке переменных в JSON-тело в Postman:

```json
{
    "user_id": "{{userId}}",
    "user_id": {{userId}}
}
```

Первая строка — правильно: строка в кавычках. Вторая — неправильно: JSON сломается. UUID — это строка, поэтому в JSON она должна быть в двойных кавычках.

## 📌 Требования

- Python 3.10+
- Доступ к sandbox-API TotalShiftLeft (URL задаётся в `.env`)

## 💡 Что показывает этот проект

- Умение переносить ручные сценарии из Postman в автоматизированные тесты
- Владение pytest: фикстуры, маркеры, параметризация, структура проекта
- Понимание разницы между ручной проверкой и автотестом: изоляция, setup/teardown, повторяемость
- Навык работы с JSON Schema для валидации контрактов API
- Осознанный подход к негативным тестам: ожидания основаны на реальном поведении сервиса, а не на предположениях
