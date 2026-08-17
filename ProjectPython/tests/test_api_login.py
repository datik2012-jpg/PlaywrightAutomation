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


def test_api_login_success(api_context: APIRequestContext) -> None:
    response = api_context.post(
        "/api/login",
        data={
            "email": "dani@example.com",
            "password": "1234567",
        },
    )

    expect(response).to_be_ok()
    assert response.status == 200
    assert response.json() == {
        "success": True,
        "token": "demo-api-token",
        "user": {"email": "dani@example.com"},
    }


def test_api_login_rejects_invalid_credentials(
    api_context: APIRequestContext,
) -> None:
    response = api_context.post(
        "/api/login",
        data={
            "email": "wrong@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status == 401
    assert response.json() == {"error": "Invalid email or password"}


def test_api_login_requires_email_and_password(
    api_context: APIRequestContext,
) -> None:
    response = api_context.post(
        "/api/login",
        data={"email": "dani@example.com"},
    )

    assert response.status == 400
    assert response.json() == {"error": "Email and password are required"}
