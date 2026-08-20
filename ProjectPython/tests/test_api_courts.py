import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import APIRequestContext, Playwright, expect


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:3000").rstrip("/")


@pytest.fixture
def api_context(playwright: Playwright) -> Iterator[APIRequestContext]:
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()


def login_and_get_token(api_context: APIRequestContext) -> str:
    response = api_context.post(
        "/api/login",
        data={"email": "dani@example.com", "password": "1234567"},
    )

    expect(response).to_be_ok()
    return response.json()["token"]


def test_get_courts_with_token(api_context: APIRequestContext) -> None:
    token = login_and_get_token(api_context)

    response = api_context.get(
        "/api/courts",
        headers={"Authorization": f"Bearer {token}"},
    )

    expect(response).to_be_ok()
    assert response.status == 200
    assert response.json() == {
        "success": True,
        "courts": [
            {
                "id": 1,
                "name": "Court A",
                "status": "Available",
                "time": "18:00",
            },
            {
                "id": 2,
                "name": "Court B",
                "status": "Available",
                "time": "18:00",
            },
        ],
    }


def test_get_courts_without_token_is_unauthorized(
    api_context: APIRequestContext,
) -> None:
    response = api_context.get("/api/courts")

    assert response.status == 401
    assert response.ok is False
    assert response.json() == {"error": "Unauthorized"}
