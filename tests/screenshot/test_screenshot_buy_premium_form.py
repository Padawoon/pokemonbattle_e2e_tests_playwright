import pytest
from playwright.sync_api import expect

from pages.premium_page import PremiumPage

@pytest.mark.parametrize(
    "test_days, snapshot_name",
    [
        ("29", "buy_premium_form_less_than_30_days.png"),
        ("155", "buy_premium_form_30_to_180_days.png"),
        ("300", "buy_premium_form_180_to_365_days.png"),
        ("366", "buy_premium_form_more_than_365_days.png")
    ]
)
def test_buy_premium_visual(page, assert_snapshot, test_days, snapshot_name):

    premium_page = PremiumPage(page)
    premium_page.open_page()

    premium_page.check_page_is_premium_page()
    premium_page.element_visible(premium_page.premium_days_input)

    premium_page.premium_days_input.press_sequentially(test_days)
    expect(premium_page.premium_per_days).to_have_attribute("style", "")

    screenshot = premium_page.buy_premium_form.screenshot()

    assert_snapshot(
        screenshot,
        snapshot_name
    )