import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.parametrize(
    "email,password,expected_status,expected_message",
    [
        (
            "dani@example.com",
            "1234567",
            200,
            None,
        ),
        (
            "dani@example.com",
            "wrong-password",
            401,
            "Invalid email or password",
        ),
        (
            "wrong@example.com",
            "1234567",
            401,
            "Invalid email or password",
        ),
        (
            "",
            "1234567",
            400,
            "Email and password are required",
        ),
    ],
)
def test_login_with_different_data(
    api_context: APIRequestContext,
    email: str,
    password: str,
    expected_status: int,
    expected_message: str | None,
) -> None:
    response = api_context.post(
        "/api/login",
        data={
            "email": email,
            "password": password,
        },
    )

    body = response.json()

    assert response.status == expected_status

    if expected_status == 200:
        assert body["success"] is True
        assert body["token"]
    else:
        assert response.ok is False
        assert body["error"] == expected_message