from collections.abc import Iterator

import pytest
from playwright.sync_api import Page


@pytest.fixture
def logged_in_page(page: Page) -> Iterator[Page]:
    print("LOGIN")

    yield page

    print("CLEANUP")


def test_booking(logged_in_page: Page) -> None:
    print("BOOKING TEST")


def test_cancel(logged_in_page: Page) -> None:
    print("CANCEL TEST")


def test_something_else(page: Page) -> None:
    print("OTHER TEST")
