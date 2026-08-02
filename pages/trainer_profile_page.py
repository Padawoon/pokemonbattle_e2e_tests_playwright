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

    @property
    def trainer_stats(self):
        return self.page.locator(".single_page_body_content_inner_box")

    @property
    def achievements(self):
        return self.page.locator(".achievements")

    @property
    def sliders(self):
        return self.page.locator(".single_page_body_content_inner_top_list_attr_one_slide")

    @property
    def pokemon_stats(self):
        return self.page.locator('//span[text()="Покеболы"]/following-sibling::*')

    @property
    def level_stats(self):
        return self.page.locator('//span[text()="Уровень"]/following-sibling::*')

    def check_page_is_profile_page(self):
        expect(self.page).to_have_url(self.URL)
        expect(self.page.get_by_text(f"ID тренера{os.getenv("TRAINER_ID")}"))

    def open_page(self):
        self.page.goto(self.URL)

