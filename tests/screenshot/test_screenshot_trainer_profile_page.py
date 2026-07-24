from playwright.sync_api import expect

from pages.trainer_profile_page import TrainerProfilePage


def test_trainer_stats_visual(page, assert_snapshot):
    profile_page = TrainerProfilePage(page)
    profile_page.open()
    