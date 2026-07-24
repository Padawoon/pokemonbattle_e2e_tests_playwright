from playwright.sync_api import expect
from pages.base_page import BasePage


class PremiumPage(BasePage):

    URL = f"{BasePage.BASE_URL}/premium"

    @property
    def heading(self):
        return self.page.get_by_role("heading", name="Pokemon Premium")

    @property
    def premium_days_input(self):
        return self.page.locator("input[name='day']")

    @property
    def go_to_payment_button(self):
        return self.page.get_by_role("button", name="Перейти к оплате")

    @property
    def cancel_premium_button(self):
        return self.page.locator("#cancel-premium")

    @property
    def cancel_premium_dialogue(self):
        return self.page.get_by_text("Вы уверены, что хотите отменить подписку?", exact=True)

    @property
    def confirm_cancel_premium_button(self):
        return self.page.locator("#cancel-go-premium")

    @property
    def cancel_premium_success_notify(self):
        return self.page.get_by_text("Вы отменили подписку :(", exact=True)

    def check_page_is_premium_page(self):
        expect(self.page).to_have_url(self.URL)
        self.element_visible(self.heading)

    def cancel_premium(self):
        self.cancel_premium_button.click()

    def confirm_cancel_premium(self):
        self.confirm_cancel_premium_button.click()



