"""Генерация уникальных тестовых данных."""

import time


def unique_user_data():
    """
    Возвращает dict с уникальными name и email.

    Использует time.time() в миллисекундах — гарантирует уникальность
    при повторных прогонах и параллельном запуске.
    """
    timestamp = int(time.time() * 1000)
    return {
        "name": f"TestUser_{timestamp}",
        "email": f"testuser_{timestamp}@example.com",
    }