import pytest
from playwright.sync_api import Page, expect


from playwright.sync_api import Page


#no best practices option (email and password are not in the init and accross the code) see second version n the bottom
class LoginPage:

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("http://127.0.0.1:3000/login")

    def login(self, email: str, password: str):
        self.page.get_by_label("email").fill(email)
        self.page.get_by_label("password").fill(password)

        self.page.get_by_role(
            "button",
            name="Login"
        ).click()


def test_invalid_password(page: Page):

    login_page = LoginPage(page)

    login_page.open()

    login_page.login(
        "qa@test.com",
        "WRONG123"
    )
    
    #more common POM style version and best practice to do is:
    class LoginPage:

        def __init__(self, page: Page):
            self.page = page
            self.email_input = page.get_by_label("email")
            self.password_input = page.get_by_label("password")
            self.login_button = page.get_by_role("button", name="Login")

        def open(self):
            self.page.goto("http://127.0.0.1:3000/login")

        def login(self, email: str, password: str):
            self.email_input.fill(email)
            self.password_input.fill(password)
            self.login_button.click()
        
        
        def test_invalid_password(page: Page):

            login_page = LoginPage(page)

            login_page.open()

            login_page.login(
            "qa@test.com",
            "WRONG123"
            )
            
            #Your next step is simple: add assertions for staying on /login and seeing “Invalid email or password”.
            expect(page).to_have_url("http://127.0.0.1:3000/login")) #so we stay in the same page cause password is wrong
                # Validation error appears
            expect(page).get_by_role("status")).to_have_text(
              "Invalid email or password"
            )
            
            
# and we can add to the POD as well
            
#But since we're practicing POM, we can improve the Page Object with login button and error message

#Add the error locator:

class LoginPage:


    def __init__(self, page: Page):
        self.page = page


        self.email_input = page.get_by_label("email")
        self.password_input = page.get_by_label("password")
        self.login_button = page.get_by_role(
            "button",
            name="Login"
        )


        self.error_message = page.get_by_role("status")

#Then the test becomes:

def test_invalid_password(page: Page):
    login_page = LoginPage(page)


    login_page.open()
    login_page.login(
        "qa@test.com",
        "WRONG123"
    )


    expect(page).to_have_url(
        "http://127.0.0.1:3000/login"
    )


    expect(
        login_page.error_message
    ).to_have_text(
        "Invalid email or password"
    )