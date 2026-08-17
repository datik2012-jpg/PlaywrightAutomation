import os

import pytest
from playwright.sync_api import Page, expect


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:3000").rstrip("/")


def login(page: Page, email: str, password: str) -> None:
    page.goto(BASE_URL)

    login_form = page.locator("#login-form")
    login_form.get_by_label("Email").fill(email)
    login_form.get_by_label("Password").fill(password)
    login_form.get_by_role("button", name="Log In").click()

    expect(page).to_have_url(f"{BASE_URL}/courts.html")


def book_court(page: Page, court_name: str, booking_time: str) -> None:
    court = page.get_by_role("article", name=court_name)

    expect(court).to_contain_text("Available")
    expect(court.get_by_text(booking_time, exact=True)).to_be_visible()

    book_button = court.get_by_role("button", name="Book")
    expect(book_button).to_be_enabled()
    book_button.click()


@pytest.mark.parametrize(
    "court_name, booking_time",
    [
        ("Court A", "18:00"),
        ("Court B", "18:00"),
    ],
)
def test_login_and_book_court(
    page: Page,
    court_name: str,
    booking_time: str,
) -> None:
    login(
        page=page,
        email="dani@example.com",
        password="1234567",
    )

    book_court(
        page=page,
        court_name=court_name,
        booking_time=booking_time,
    )
