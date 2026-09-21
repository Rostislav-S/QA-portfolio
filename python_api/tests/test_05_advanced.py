"""Продвинутые проверки: глубокая валидация схемы."""

import re

import pytest
from jsonschema import validate

from schemas.user import USERS_LIST_RESPONSE_SCHEMA


UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

ISO8601_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"
)

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@pytest.mark.advanced
def test_users_deep_schema_validation(api_client):
    """5.1 GET /users — глубокая валидация схемы ответа."""
    response = api_client.get(
        f"{api_client.base_url}/users",
        params={"limit": 5},
    )

    assert response.status_code == 200

    data = response.json()

    # Общая схема
    validate(instance=data, schema=USERS_LIST_RESPONSE_SCHEMA)

    users = data["data"]

    # ID уникальны в рамках страницы
    ids = [u["id"] for u in users]
    assert len(ids) == len(set(ids)), "ID должны быть уникальны"

    # Форматы полей
    for user in users:
        assert UUID_PATTERN.match(user["id"]), (
            f"ID не соответствует UUID: {user['id']}"
        )
        assert EMAIL_PATTERN.match(user["email"]), (
            f"Email невалиден: {user['email']}"
        )
        assert ISO8601_PATTERN.match(user["created_at"]), (
            f"created_at не ISO 8601: {user['created_at']}"
        )
        assert user["role"] in ("user", "admin"), (
            f"role вне допустимых значений: {user['role']}"
        )

    # Количество элементов не превышает limit
    assert len(users) <= data["pagination"]["limit"]