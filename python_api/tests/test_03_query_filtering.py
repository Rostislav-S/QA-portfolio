"""Проверка query-параметров: фильтрация и пагинация."""

import pytest
from jsonschema import validate

from schemas.pagination import PAGINATION_SCHEMA


@pytest.mark.query
def test_products_filter_by_category(api_client):
    """3.1 GET /products?category=books — фильтрация."""
    response = api_client.get(
        f"{api_client.base_url}/products",
        params={"category": "books", "limit": 5},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert isinstance(data["data"], list)

    # Количество не превышает limit
    assert len(data["data"]) <= 5, (
        f"Получено {len(data['data'])} товаров при limit=5"
    )

    # Все товары категории books
    for product in data["data"]:
        assert product["category"] == "books", (
            f"Товар {product.get('id')} не из категории books"
        )

    # Пагинация отражает фильтр
    validate(instance=data["pagination"], schema=PAGINATION_SCHEMA)
    assert data["pagination"]["limit"] == 5
    assert data["pagination"]["page"] == 1


@pytest.mark.query
def test_products_pagination(api_client):
    """3.2 GET /products?page=2&limit=5 — пагинация."""
    response = api_client.get(
        f"{api_client.base_url}/products",
        params={"page": 2, "limit": 5},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    pagination = data["pagination"]

    validate(instance=pagination, schema=PAGINATION_SCHEMA)

    # Отражает запрошенную страницу
    assert pagination["page"] == 2
    assert pagination["limit"] == 5

    # hasPrev = True для второй страницы
    assert pagination["hasPrev"] is True

    # Количество не превышает limit
    assert len(data["data"]) <= 5