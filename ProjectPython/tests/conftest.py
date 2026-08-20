import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import APIRequestContext, Playwright


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:3000").rstrip("/")


@pytest.fixture
def api_context(playwright: Playwright) -> Iterator[APIRequestContext]:
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()
