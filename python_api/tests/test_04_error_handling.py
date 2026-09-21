"""Негативные сценарии и обработка ошибок.

Соответствует папке 04_Error_Handling в Postman-коллекции.

Каждый тест проверяет один негативный сценарий:
- серверная ошибка (500)
- таймаут (задержка ответа)
- невалидный формат UUID в path-параметре
- несуществующий ресурс
- невалидный формат product_id в теле POST-запроса
"""

import pytest
from jsonschema import validate

from schemas.error import (
    FASTIFY_ERROR_SCHEMA,
    GENERIC_ERROR_SCHEMA,
)


# ---------------------------------------------------------------------------
# 4.1 GET /users?error=500 — Server Error
# ---------------------------------------------------------------------------

@pytest.mark.error
def test_server_error_500(api_client):
    """4.1 GET /users?error=500 — симуляция серверной ошибки."""
    response = api_client.get(
        f"{api_client.base_url}/users",
        params={"error": 500},
    )

    assert response.status_code == 500, (
        f"Ожидался 500, получен {response.status_code}"
    )

    data = response.json()

    # Ошибка должна содержать error или message
    has_error = "error" in data or "message" in data
    assert has_error, "Ответ должен содержать error или message"

    # Стек вызовов не должен утекать
    body = response.text.lower()
    assert "stack" not in body, "Ответ не должен содержать стек"
    assert "at object." not in body, "Ответ не должен содержать внутренние пути"


# ---------------------------------------------------------------------------
# 4.2 GET /users?delay=2000 — Timeout Behavior
# ---------------------------------------------------------------------------

@pytest.mark.error
def test_timeout_behavior(api_client):
    """4.2 GET /users?delay=2000 — задержка ответа."""
    response = api_client.get(
        f"{api_client.base_url}/users",
        params={"delay": 2000},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True

    # Задержка действительно применена (2 секунды, с небольшим запасом)
    elapsed = response.elapsed.total_seconds()
    assert elapsed >= 1.8, (
        f"Задержка не применена: {elapsed} сек"
    )


# ---------------------------------------------------------------------------
# 4.3 GET /users/{invalid-id} — Invalid UUID Format
# ---------------------------------------------------------------------------

@pytest.mark.error
def test_invalid_uuid_format(api_client):
    """4.3 GET /users/999999 — невалидный формат UUID в path."""
    response = api_client.get(f"{api_client.base_url}/users/999999")

    assert response.status_code == 400, (
        f"Ожидался 400, получен {response.status_code}"
    )

    data = response.json()

    # Схема Fastify-ошибки
    validate(instance=data, schema=FASTIFY_ERROR_SCHEMA)

    assert data["statusCode"] == 400
    assert data["code"] == "FST_ERR_VALIDATION"
    assert data["error"] == "Bad Request"

    # Сообщение указывает на формат UUID
    assert "uuid" in data["message"].lower(), (
        f"Сообщение не содержит 'uuid': {data['message']}"
    )

    # Стек не раскрыт
    assert "stack" not in response.text.lower()


# ---------------------------------------------------------------------------
# 4.4 GET /users/{uuid} — Not Found
# ---------------------------------------------------------------------------

@pytest.mark.error
def test_not_found(api_client):
    """4.4 GET /users/{uuid} — несуществующий ресурс."""
    # UUID валиден по формату, но не существует в sandbox
    url = f"{api_client.base_url}/users/00000000-0000-0000-0000-000000000000"
    response = api_client.get(url)

    assert response.status_code == 404, (
        f"Ожидался 404, получен {response.status_code}"
    )

    data = response.json()

    # Универсальная схема ошибки
    validate(instance=data, schema=GENERIC_ERROR_SCHEMA)

    # Стек не раскрыт
    assert "stack" not in response.text.lower()


# ---------------------------------------------------------------------------
# 4.5 POST /orders — Invalid product_id Format
# ---------------------------------------------------------------------------

@pytest.mark.error
def test_order_invalid_product_id(api_client, created_user):
    """
    4.5 POST /orders — невалидный формат product_id.

    Fastify-валидация схемы тела отсекает запрос до бизнес-логики:
    product_id должен быть UUID-строкой, а мы передаём "not-a-uuid".

    Аналог 4.3 — только для POST и поля product_id.
    """
    response = api_client.post(
        f"{api_client.base_url}/orders",
        json={
            "user_id": created_user["id"],       # валидный UUID
            "product_id": "not-a-uuid",          # невалидный формат
            "quantity": 1,
        },
    )

    assert response.status_code == 400, (
        f"Ожидался 400, получен {response.status_code}. "
        f"Тело: {response.text}"
    )

    data = response.json()

    # Сообщение указывает на product_id и формат uuid
    assert "message" in data, "Ответ должен содержать message"
    assert "product_id" in data["message"].lower(), (
        f"Сообщение не содержит 'product_id': {data['message']}"
    )
    assert "uuid" in data["message"].lower(), (
        f"Сообщение не содержит 'uuid': {data['message']}"
    )

    # Стек не раскрыт
    assert "stack" not in response.text.lower()