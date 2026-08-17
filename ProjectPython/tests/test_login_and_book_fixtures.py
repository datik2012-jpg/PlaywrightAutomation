import os
from typing import TypedDict

import pytest
from playwright.sync_api import Page, expect


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:3000").rstrip("/")


class Credentials(TypedDict):
    email: str
    password: str


class Booking(TypedDict):
    court_name: str
    booking_time: str


@pytest.fixture
def credentials() -> Credentials:
    return {
        "email": "dani@example.com",
        "password": "1234567",
    }


@pytest.fixture
def logged_in_page(page: Page, credentials: Credentials) -> Page:
    page.goto(BASE_URL)

    login_form = page.locator("#login-form")
    login_form.get_by_label("Email").fill(credentials["email"])
    login_form.get_by_label("Password").fill(credentials["password"])
    login_form.get_by_role("button", name="Log In").click()

    expect(page).to_have_url(f"{BASE_URL}/courts.html")
    return page


@pytest.fixture(
    params=[
        {"court_name": "Court A", "booking_time": "18:00"},
        {"court_name": "Court B", "booking_time": "18:00"},
    ],
    ids=["court-a-18-00", "court-b-18-00"],
)
def booking(request: pytest.FixtureRequest) -> Booking:
    return request.param


def test_login_and_book_with_fixtures(
    logged_in_page: Page,
    booking: Booking,
) -> None:
    court = logged_in_page.get_by_role(
        "article",
        name=booking["court_name"],
    )

    expect(court).to_contain_text("Available")
    expect(
        court.get_by_text(booking["booking_time"], exact=True)
    ).to_be_visible()

    book_button = court.get_by_role("button", name="Book")
    expect(book_button).to_be_enabled()
    book_button.click()
