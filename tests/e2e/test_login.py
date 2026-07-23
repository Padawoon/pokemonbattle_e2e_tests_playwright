import allure
from playwright.sync_api import Page, expect
from pages.main_page import MainPage
from pages.login_page import LoginPage


def test_login(page: Page):
    with allure.step("Переход на главную страницу"):
        login_page = LoginPage(page)
        login_page.open("https://pokemonbattle.ru/")

    with allure.step("Редирект на страницу авторизации"):
        login_page.check_page_is_login_page()

    with allure.step("Авторизация с валидными кредами"):
        login_page.login()

    with allure.step("Проверка корректной авторизации тестового тренера"):
        main_page = MainPage(page)
        main_page.check_page_is_main_page()
        expect(main_page.trainer_badge).to_be_visible()