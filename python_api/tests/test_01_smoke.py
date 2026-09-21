"""Smoke-тесты: проверка доступности ключевых эндпоинтов."""

import pytest
from jsonschema import validate

from schemas.user import USERS_LIST_RESPONSE_SCHEMA
from schemas.pagination import PAGINATION_SCHEMA


@pytest.mark.smoke
def test_users_health_check(api_client):
    """1.1 GET /users — базовая проверка доступности."""
    response = api_client.get(f"{api_client.base_url}/users")

    # Статус
    assert response.status_code == 200, (
        f"Ожидался 200, получен {response.status_code}"
    )

    data = response.json()

    # Флаг success
    assert data["success"] is True, "Флаг success должен быть True"

    # Массив data
    assert isinstance(data["data"], list), "Поле data должно быть массивом"

    # Схема ответа
    validate(instance=data, schema=USERS_LIST_RESPONSE_SCHEMA)

    # Схема пагинации
    validate(instance=data["pagination"], schema=PAGINATION_SCHEMA)


@pytest.mark.smoke
def test_products_health_check(api_client):
    """1.2 GET /products — базовая проверка доступности."""
    response = api_client.get(f"{api_client.base_url}/products")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert "pagination" in data

    # Схема пагинации
    validate(instance=data["pagination"], schema=PAGINATION_SCHEMA)