import pytest
from playwright.sync_api import expect

from pages.payments_page import PaymentsPage
from pages.premium_page import PremiumPage


def test_empty_card_details_form_empty_visual(page, assert_snapshot):

    premium_page = PremiumPage(page)
    payments_page = PaymentsPage(page)

    premium_page.open_page()
    premium_page.check_page_is_premium_page()
    premium_page.premium_days_input.fill("15")
    premium_page.go_to_payment_button.click()

    payments_page.check_page_is_payments_page()

    screenshot = payments_page.card_details_form.screenshot()

    assert_snapshot(
        screenshot,
        "empty_card_details_form.png"
    )

def test_filled_card_details_form_visual(page, assert_snapshot):

    premium_page = PremiumPage(page)
    payments_page = PaymentsPage(page)

    premium_page.open_page()
    premium_page.check_page_is_premium_page()
    premium_page.premium_days_input.fill("15")
    premium_page.go_to_payment_button.click()

    payments_page.check_page_is_payments_page()
    payments_page.fill_card_details()
    payments_page.page.keyboard.press("Tab")
    expect(payments_page.pay_button).to_have_class("style_1_base_button_payment")


    screenshot = payments_page.card_details_form.screenshot()

    assert_snapshot(
        screenshot,
        "filled_card_details_form.png"
    )

@pytest.mark.parametrize(
    "card_number, expiry_date, snapshot_name",
    [
        ("0000000000000000", None, "invalid_card_number.png"),
        (None, "25/25", "invalid_expiry.png")
    ],
    ids=["invalid_card", "invalid_expiry"],
)
def test_invalid_invalid_inputs_visual(page, assert_snapshot, card_number, expiry_date, snapshot_name):

    premium_page = PremiumPage(page)
    payments_page = PaymentsPage(page)

    premium_page.open_page()
    premium_page.check_page_is_premium_page()
    premium_page.premium_days_input.fill("15")
    premium_page.go_to_payment_button.click()

    payments_page.check_page_is_payments_page()

    if card_number is not None:
        payments_page.card_number_input.press_sequentially(card_number, delay=50)

    if expiry_date is not None:
        (payments_page.card_expiry_input.press_sequentially(expiry_date, delay=50))

    screenshot = payments_page.card_details_form.screenshot()

    assert_snapshot(
        screenshot,
        snapshot_name
    )

