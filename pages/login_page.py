import os

from dotenv import load_dotenv
from playwright.sync_api import expect
from pages.base_page import BasePage


class LoginPage(BasePage):

    URL = f"{BasePage.BASE_URL}/login"

    @property
    def email_input(self):
        return self.page.get_by_role("textbox", name="Почта")

    @property
    def password_input(self):
        return self.page.get_by_role("textbox", name="Пароль")

    @property
    def login_button(self):
        return self.page.get_by_role("button", name="Войти")

    def open_page(self):
        self.page.goto(self.URL)

    def login(self):
        self.email_input.fill(os.getenv("LOGIN"))
        self.password_input.fill(os.getenv("PASSWORD"))
        self.login_button.click()

    def check_page_is_login_page(self):
        expect(self.page).to_have_url(self.URL)

