"""CRUD-операции на ресурсе users."""

import re

import pytest
from jsonschema import validate

from schemas.user import (
    SINGLE_USER_RESPONSE_SCHEMA,
    USER_SCHEMA,
)


UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


@pytest.mark.crud
def test_create_user(api_client, unique_user):
    """2.1 POST /users — создание пользователя."""
    response = api_client.post(
        f"{api_client.base_url}/users",
        json=unique_user,
    )

    # Статус
    assert response.status_code == 201, (
        f"Ожидался 201, получен {response.status_code}"
    )

    data = response.json()

    # Флаг success
    assert data["success"] is True

    # Схема ответа
    validate(instance=data, schema=SINGLE_USER_RESPONSE_SCHEMA)

    user = data["data"]

    # ID — валидный UUID
    assert UUID_PATTERN.match(user["id"]), (
        f"ID должен быть UUID, получен: {user['id']}"
    )

    # Данные совпадают с отправленными
    assert user["name"] == unique_user["name"]
    assert user["email"] == unique_user["email"]

    # Дополнительные поля
    assert user["role"] == "user"
    assert "created_at" in user


@pytest.mark.crud
def test_read_user(api_client, created_user):
    """2.2 GET /users/{id} — чтение созданного пользователя."""
    response = api_client.get(
        f"{api_client.base_url}/users/{created_user['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    validate(instance=data, schema=SINGLE_USER_RESPONSE_SCHEMA)

    user = data["data"]

    # ID совпадает с запрошенным
    assert user["id"] == created_user["id"]

    # Данные полные
    for field in ("name", "email", "role", "created_at"):
        assert field in user, f"Отсутствует поле {field}"


@pytest.mark.crud
def test_update_user(api_client, created_user):
    """2.3 PATCH /users/{id} — частичное обновление."""
    new_name = "Updated Name"

    response = api_client.patch(
        f"{api_client.base_url}/users/{created_user['id']}",
        json={"name": new_name},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    user = data["data"]

    # Имя обновлено
    assert user["name"] == new_name, (
        f"Ожидалось name={new_name}, получено {user['name']}"
    )

    # Остальные поля не изменились
    assert user["email"] == created_user["email"]
    assert user["role"] == created_user["role"]
    assert user["id"] == created_user["id"]


@pytest.mark.crud
def test_delete_user(api_client, created_user):
    """2.4 DELETE /users/{id} — удаление пользователя."""
    response = api_client.delete(
        f"{api_client.base_url}/users/{created_user['id']}"
    )

    # Статус 204
    assert response.status_code == 204, (
        f"Ожидался 204, получен {response.status_code}"
    )

    # Тело пустое
    assert response.text == "", "Тело ответа 204 должно быть пустым"

    # Проверка, что ресурс действительно удалён
    check = api_client.get(
        f"{api_client.base_url}/users/{created_user['id']}"
    )
    assert check.status_code == 404, (
        "После DELETE ресурс должен возвращать 404"
    )