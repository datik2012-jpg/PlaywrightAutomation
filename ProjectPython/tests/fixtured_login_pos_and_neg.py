import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def username():
    return "Dani"

@pytest.fixture
def nikname():
    return "Zhako"


def test_username(username):
    assert username == "Dani"

def test_nikname(nikname):
    assert nikname == "Zhako"
    
#def test_web_page_title(page: Page):
    #page.goto("http://127.0.0.1:3000")    
    #expect(page).to_have_title("Welcome Back | Demo Login")
    
@pytest.fixture
def login_page(page: Page):
    page.goto("http://127.0.0.1:3000")
    return page   

def test_login_page_visibility(login_page: Page):
    
    expect(login_page).to_have_title("Welcome Back | Demo Login")
    
    login_page.screenshot(path="D:/GitHub/PlaywrightAutomation/ProjectA/notes/booking_failure.png")
    
    #intro is visible
    intro = login_page.locator(".intro")
    expect(intro).to_be_visible()
    expect(intro).to_have_text("Enter your details to access your account.")
    
    #login form is visible 
    login_form = login_page.locator("#login-form")
    expect(login_form).to_have_count(1)
    expect(login_form).to_be_visible()
    
    #email is visible and password (we can use login-form as well)
    email = login_page.get_by_label("email")
    expect(email).to_be_visible()
    
    #passwrod is visible
    password = login_page.get_by_label("password ")
    expect(password ).to_be_visible()
    
    #buttin exist and visible
    button = login_page.get_by_role("button", name="Log In")
    expect(button).to_be_visible()
    
#positive test
def test_do_login(login_page: Page):
        login_page.get_by_label("email").fill("dani@walla.com")
        login_page.get_by_label("password").fill("noqwerty")
        login_page.get_by_role("button", name="Log In").click()
        
        #verify navigation
        
        expect(login_page).to_have_url("http://127.0.0.1:3000/courts.html")
        
        #verify head is exit in the courts page
        heading = login_page.get_by_role("heading", name="Available courts",)
        expect(heading).to_be_visible()

#negative test       
def test_login_with_invalid_email(login_page: Page):
    login_page.get_by_label("Email").fill("invalid-email")
    login_page.get_by_label("Password").fill("noqwerty")
    login_page.get_by_role("button", name="Log In").click()

    # User remains on login page
    expect(login_page).to_have_url(
        "http://127.0.0.1:3000/"
    )

    # Validation error appears
    expect(login_page.get_by_role("status")).to_have_text(
        "Enter a valid email and a password of at least 6 characters."
    )

    # Courts page is not displayed
    expect(
        login_page.get_by_role(
            "heading",
            name="Available courts",
        )
    ).not_to_be_visible()        

@pytest.mark.parametrize(
    "email, password",
    [
        ("dani@walla.co.il", "noqwerty"),
        ("tim@gmail.com", "zagafer123"),
        ("kola@hotmail.com", "zfghtr34"),
    ],
)
def test_login_with_parametrize(
    login_page: Page,
    email: str,
    password: str,
):
        login_page.get_by_label("email").fill(email)
        login_page.get_by_label("password").fill(password)
        login_page.get_by_role("button", name="Log In").click()
        
        #verify navigation
        
        expect(login_page).to_have_url("http://127.0.0.1:3000/courts.html")
 
if __name__ == "__main__":
    print("hello fixtures")
