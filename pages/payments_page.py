import os
import re

from dotenv import load_dotenv
from playwright.sync_api import expect
from pages.base_page import BasePage

load_dotenv()


class PaymentsPage(BasePage):

    URL = f"{BasePage.BASE_URL}/payment/*"

    @property
    def card_number_input(self):
        return self.page.get_by_role("textbox", name="0000 0000 0000 0000")

    @property
    def card_expiry_input(self):
        return self.page.get_by_role("textbox", name="00/00")

    @property
    def card_cvc_input(self):
        return self.page.get_by_placeholder("000", exact=True)

    @property
    def card_holder_input(self):
        return self.page.get_by_placeholder("GERMAN DOLNIKOV")

    @property
    def pay_button(self):
        return self.page.get_by_role("button", name="Оплатить")

    @property
    def card_details_form(self):
        return self.page.locator('.payment_form_card_form')

    def check_page_is_payments_page(self):
        expect(self.page).to_have_url(re.compile(r"/payment/.+"))
        self.element_visible(self.pay_button)

    def open_page(self):
        self.page.goto(self.URL)

    def fill_card_details(
            self,
            number: str | None = None,
            expiry: str | None = None,
            cvc: str | None = None,
            holder: str | None = None
    ):
        number = number or os.getenv("VISA")
        expiry = expiry or os.getenv("DUE_DATE")
        cvc = cvc or os.getenv("SUCCESS_CVV")
        holder = holder or os.getenv("CARD_NAME")

        self.card_number_input.press_sequentially(number, delay=50)
        self.card_expiry_input.fill(expiry)
        self.card_cvc_input.fill(cvc)
        self.card_holder_input.press_sequentially(holder, delay=50)

    def submit_payment(self):
        self.pay_button.click()