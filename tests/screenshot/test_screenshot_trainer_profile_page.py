import re

from playwright.sync_api import expect

from pages.trainer_profile_page import TrainerProfilePage


def test_trainer_stats_visual(page, assert_snapshot):
    profile_page = TrainerProfilePage(page)
    profile_page.open_page()

    profile_page.check_page_is_profile_page()
    expect(profile_page.beginning_achievement).to_have_class(re.compile(r"active"))

    screenshot = profile_page.trainer_stats.screenshot(
        mask=[
            profile_page.pokemon_stats,
            profile_page.level_stats,
            profile_page.achievements
        ],
        mask_color="#07fa02"
    )

    assert_snapshot(
        screenshot,
        "trainer_stats.png"
        # порог дефолтный
    )