import os

from playwright.sync_api import expect

from pages.base_page import BasePage


class MainPage(BasePage):

    URL = BasePage.BASE_URL

    @property
    def trainer_badge(self):
        return self.page.get_by_role("link", name=f"ID {os.getenv("TRAINER_ID")} логотип")

    def check_page_is_main_page(self):
        expect(self.page).to_have_url(f"{self.URL}/")
