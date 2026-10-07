from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email = page.locator("#email")
        self.password = page.locator("#password")
        self.submit = page.locator("#loginButton")
        self.error = page.locator(".error")

    def open(self):
        self.page.goto("/#/login")
        expect(self.email).to_be_visible()
        return self

    def login(self, email: str, password: str):
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
