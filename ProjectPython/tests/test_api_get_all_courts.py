import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import APIRequestContext, Playwright, expect

#run the test: python -m pytest tests/test_api_login.py -v


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:3000").rstrip("/")


@pytest.fixture
def api_context(playwright: Playwright) -> Iterator[APIRequestContext]:
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()
    
def test_body_login(api_context: APIRequestContext) -> None:
    response = api_context.post("api/login", data={"email": "dani@example.com", "password": "1234567"},)
    expect(response).to_be_ok()
    assert response.status == 200
    body = response.json()
    print(body)
    
    #test
    assert body["success"] is not None
    assert body["token"] is not None
    assert body["token"] != ""
    assert body["user"]["email"] == "dani@example.com"
    
#negative api testing -server.js is set return 401 error
def test_invalid_body_login(api_context: APIRequestContext) -> None:
    response = api_context.post("api/login", data={"email": "dani@example.com", "password": "nopassword"},)
    assert response.status == 401
    assert response.ok is False
    body = response.json()
    print(body)  
    
    #test which can be broken tomorrow when decide to change responce json and add new data
    #assert response.json() == {'error': 'Invalid email or password'}
    
    #better do this
    assert body["error"] == "Invalid email or password"
    
    
def test_get_all_courts(api_context: APIRequestContext) -> None:
    response_login = api_context.post("api/login", data={"email": "dani@example.com", "password": "1234567"},)    
    
    body = response_login.json()

    token = body["token"]
    
    print(f"Print body: {body}")
    print(f"token is: {token}")
    
    
    #get all courts
    
    response_courts = api_context.get(
      "/api/courts",
      headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response_courts.status == 200
    assert response_courts.ok is True

    courts_body = response_courts.json()
    assert courts_body["success"] is True
    assert len(courts_body["courts"]) == 2

    print(response_courts.status)
    print(response_courts.text())
    
    
    
def test_negative_token_courts(api_context: APIRequestContext) -> None:
    response_login = api_context.post("api/login", data={"email": "dani@example.com", "password": "1234567"},)    
    
    body = response_login.json()

    token = "" #no token
    
    print(f"Print body: {body}")
    print(f"token is: {token}")
    
    
    #get all courts
    
    response_courts = api_context.get(
      "/api/courts",
      headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response_courts.status == 401
    assert response_courts.ok is False
    assert response_courts.json()["error"] == "Unauthorized"

    courts_body = response_courts.json()

    print(response_courts.status)
    print(response_courts.text())    