import os
from playwright.sync_api import expect
from pages.base_page import BasePage


class TrainerProfilePage(BasePage):
    URL = f"{BasePage.BASE_URL}/trainer/{os.getenv("TRAINER_ID")}"

    @property
    def premium_button(self):
        return self.page.get_by_text("Pokemon Premium")

    @property
    def beginning_achievement(self):
        return self.page.locator("#beginning")

    def check_page_is_profile_page(self):
        expect(self.page).to_have_url(self.URL)
        expect(self.page.get_by_text(f"ID тренера{os.getenv("TRAINER_ID")}"))