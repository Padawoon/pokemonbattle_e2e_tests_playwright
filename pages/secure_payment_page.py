import os
from dotenv import load_dotenv
from playwright.sync_api import expect
from pages.base_page import BasePage

load_dotenv()

class SecurePaymentPage(BasePage):

    URL = f"{BasePage.BASE_URL}/payment_3ds"
    SUCCESS_URL = f"{BasePage.BASE_URL}/payment_success"

    @property
    def otp_input(self):
        # там всего один текстбокс, пусть будет так
        return self.page.get_by_role("textbox")

    @property
    def submit_button(self):
        return self.page.get_by_role("button", name="Оплатить")

    @property
    def success_payment_notify(self):
        return self.page.get_by_text("Покупка прошла успешно")

    @property
    def open_receipt_button(self):
        return self.page.locator("button.payment_receipt_open_button_icon")

    def check_page_is_secure_payment_page(self):
        expect(self.page).to_have_url(self.URL)
        self.element_visible(self.otp_input)

    def check_page_is_success_payment_page(self):
        expect(self.page).to_have_url(self.SUCCESS_URL)
        self.element_visible(self.success_payment_notify)

    def confirm_payment(self, code: str | None = None):
        code = code or os.getenv("SECURE_CODE")
        self.otp_input.fill(code)
        self.submit_button.click()

