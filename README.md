# QA Engineer Portfolio — Skorobogatov Rostislav

> A showcase of QA skills through practical examples: SQL, API testing, and Python automation.

[![rost-s@yandex.ru](https://img.shields.io/badge/Email-Contact-red)](mailto:rost-s@yandex.ru)

## 👋 About Me

Manual QA Engineer with 1 year 9 months of experience testing web, mobile (Android/iOS), and backend services in a product company (healthcare and pharmacy retail). My move into QA was a deliberate step from a related technical field — I wanted to directly influence product quality and verify how systems behave at every layer.

I test across the full stack: frontend (UI/UX, responsiveness, cross-browser), backend (REST API, data validation, error handling), and mobile apps. I work with a distributed system of microservices — authentication and user management, an admin panel for doctors, mobile app integration, and external services for schedules and appointment booking.

I have hands-on experience with Kafka: tested SMS, push, and email delivery through message queues, verifying message formation, routing, and delivery across business scenarios. For monitoring I use Lens (pods, logs), Grafana (Loki, Tempo, Prometheus), and Sentry (production errors), plus Charles Proxy and Chrome DevTools for traffic analysis and debugging.

I write SQL queries (JOINs, aggregates, subqueries) to validate data integrity via DBeaver, and work with APIs through Postman and Swagger — building collections with pre-request and post-response scripts for automated validation. I also write Python autotests with pytest and requests, validating API contracts with JSON Schema.

My previous 12 years managing complex technical systems in oil and gas taught me to structure processes, quickly grasp new architectures, and surface risks and ambiguities during requirements analysis.

Currently growing toward API and integration testing, and applying AI tools for workflow optimization (within security policies).

**Stack:** SQL · Postman · Swagger · Python · pytest · requests · jsonschema · DBeaver · Charles Proxy · Chrome DevTools · Grafana · Sentry · Lens · Kafka · GitLab · Jira · Zephyr Scale · Confluence

## 📁 Portfolio Structure

| Directory | Contents | Skills Demonstrated |
|:---|:---|:---|
| [`sql/`](./sql/) | SQL queries for data validation: filtering, aggregation, JOINs, consistency checks | Database work, writing validation queries |
| [`postman/`](./postman/) | Postman collection covering smoke, CRUD, query params, E2E workflows, error handling, and advanced scripts | API testing, collection design, automated validation |
| [`python_api/`](./python_api/) | Python autotests for the same REST API: pytest, requests, JSON Schema validation | Test automation, fixture design, contract validation |

## 🔍 Work Samples

### 🗄️ SQL

Practical SQL queries for validating data in a flight booking database (PostgreSQL). The queries cover filtering, date handling, aggregation, multiple JOINs, and consistency checks.

- [`Блок 1.sql`](./sql/Блок%201.sql) — single queries and data validation: filtering, NULL checks, aggregation with HAVING
- [`Блок 2.sql`](./sql/Блок%202.sql) — multiple JOINs and consistency checks: orphaned records, missing boarding passes
- [`README.ru.md`](./sql/README.ru.md) — overview of the SQL section, table schema, and skills demonstrated

### 📡 Postman

A single demo collection for the **TotalShiftLeft REST API** sandbox, designed as a Middle-level API testing portfolio. It covers the full testing workflow: from smoke checks to E2E scenarios with data passing between requests.

**Collection structure:**

| Folder | Purpose | What it demonstrates |
|:---|:---|:---|
| `01_Smoke` | Health checks for key endpoints | Status codes, response structure, pagination schema |
| `02_CRUD_Users` | Full CRUD cycle: Create → Read → Update → Delete | Dynamic data generation, variable passing, UUID validation, partial updates |
| `03_Query_Filtering` | Query parameters: filtering and pagination | Response-to-filter consistency, pagination logic |
| `04_Error_Handling` | Negative scenarios: 500, timeout, invalid UUID, 404, invalid product_id | Error structure, stack trace leakage, validation layers (routing → business logic) |
| `05_Advanced_Scripts` | Deep JSON Schema validation | Formats (uuid, email, ISO 8601), enums, uniqueness, regex |
| `99_Cleanup` | Service folder: resets collection variables | Idempotency, `pm.execution.skipRequest()` |

**Key techniques used:**

- Pre-request scripts for dynamic test data (`Date.now()`-based unique names/emails)
- Passing variables between requests (`userId` set in POST, used in GET/PATCH/DELETE)
- JSON Schema validation via `pm.response.to.have.jsonSchema()`
- Negative testing across validation layers: routing → business logic
- Collection-level tests: Content-Type, response time, `success` flag presence
- Idempotency: cleanup folder resets state so the collection can be re-run without manual cleanup

- [`TotalShiftLeft REST API — QA Portfolio (Middle).postman_collection.json`](./postman/TotalShiftLeft%20REST%20API%20—%20QA%20Portfolio%20(Middle).postman_collection.json) — collection file
- [`README.ru.md`](./postman/README.ru.md) — detailed walkthrough of the collection structure and test logic

### 🐍 Python API

Python autotests for the same TotalShiftLeft REST API, written with pytest and requests. The project mirrors the Postman collection 1:1 — same structure, same scenarios — but as automated tests.

**Test coverage (14 tests):**

| Module | Purpose | Tests |
|:---|:---|:---|
| `test_01_smoke.py` | Health checks for key endpoints | 2 |
| `test_02_crud_users.py` | Full CRUD cycle with `created_user` fixture | 4 |
| `test_03_query_filtering.py` | Filtering and pagination via query params | 2 |
| `test_04_error_handling.py` | Negative scenarios: 500, timeout, invalid UUID, 404, invalid product_id | 5 |
| `test_05_advanced.py` | Deep JSON Schema validation | 1 |

**Key techniques used:**

- `requests.Session` fixture for shared headers and base URL
- `created_user` fixture with `yield` for setup/teardown isolation
- JSON Schema validation via `jsonschema.validate()`, schemas stored separately in `schemas/`
- pytest markers (`smoke`, `crud`, `query`, `error`, `advanced`) for running subsets
- HTML reports via `pytest-html`

- [`tests/`](./python_api/tests/) — test modules
- [`README.ru.md`](./python_api/README.ru.md) — detailed walkthrough of the project structure, coverage, and debugging history

## 🛠️ Tools

| Category | Tools |
|:---|:---|
| Test Management | Jira, Zephyr Scale, Confluence |
| API | Postman, Swagger |
| Automation | Python, pytest, requests, jsonschema |
| Databases | PostgreSQL, DBeaver |
| Monitoring | Grafana, Sentry, Lens |
| Version Control | GitLab |

## 📌 How to Use This Portfolio

1. Pick a directory of interest (e.g., `sql/`, `postman/`, or `python_api/`)
2. Read the README inside — it explains what each artifact demonstrates
3. To run the Postman collection: import the `*.postman_collection.json` file into Postman and run it through the Collection Runner in sequential order
4. To run the Python tests: follow the setup instructions in `python_api/README.ru.md`

## 📬 Contact

- Email: rost-s@yandex.ru
- Telegram: @RiseNglory_FR