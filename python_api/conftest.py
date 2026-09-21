"""Фикстуры проекта."""

import os
import pytest
import requests
from dotenv import load_dotenv

from helpers.data import unique_user_data as make_unique_user_data

load_dotenv()


# ---------------------------------------------------------------------------
# Конфигурация
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def base_url():
    """Базовый URL API из .env."""
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def request_timeout():
    """Таймаут HTTP-запросов из .env (по умолчанию 10 сек)."""
    return int(os.getenv("REQUEST_TIMEOUT", "10"))


# ---------------------------------------------------------------------------
# HTTP-клиент
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def api_client(base_url, request_timeout):
    """
    Сессия requests с общими заголовками.

    Создаётся один раз на весь прогон.
    Автоматически закрывается после завершения всех тестов.
    """
    session = requests.Session()
    session.headers.update({
        "X-Client": os.getenv("CLIENT_HEADER", "Python-QA-Portfolio"),
        "Accept": "application/json",
    })
    session.base_url = base_url
    session.timeout = request_timeout

    yield session
    session.close()


# ---------------------------------------------------------------------------
# Тестовые данные
# ---------------------------------------------------------------------------

@pytest.fixture
def unique_user():
    """
    Уникальные name и email для одного теста.

    Возвращает dict вида:
        {"name": "TestUser_...", "email": "testuser_...@example.com"}
    """
    return make_unique_user_data()


# ---------------------------------------------------------------------------
# Создание и удаление пользователя
# ---------------------------------------------------------------------------

@pytest.fixture
def created_user(api_client, unique_user):
    """
    Создаёт пользователя до теста и удаляет после.

    Возвращает dict с данными созданного пользователя:
        {"id": "...", "name": "...", "email": "...", "role": "...", "created_at": "..."}

    После теста пытается удалить пользователя.
    Если удаление не удалось — не падает, а лишь логирует.
    """
    response = api_client.post(
        f"{api_client.base_url}/users",
        json=unique_user,
        timeout=api_client.timeout,
    )

    assert response.status_code == 201, (
        f"Не удалось создать пользователя. "
        f"Статус: {response.status_code}, тело: {response.text}"
    )

    user = response.json()["data"]

    yield user

    # cleanup
    try:
        api_client.delete(
            f"{api_client.base_url}/users/{user['id']}",
            timeout=api_client.timeout,
        )
    except requests.RequestException as e:
        print(f"[cleanup] Не удалось удалить пользователя {user['id']}: {e}")