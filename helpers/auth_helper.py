import os

import allure
from playwright.sync_api import Page, expect


def login(page: Page):
    with allure.step("Переход на главную страницу"):
        page.goto('https://pokemonbattle.ru')
        expect(page).to_have_title("Битва Покемонов")

    with allure.step("Редирект на страницу авторизации"):
        page.wait_for_url("**/login")

    with allure.step("Авторизация с валидными кредами"):
        page.get_by_role("textbox", name="Почта").fill(os.getenv("LOGIN"))
        page.get_by_role("textbox", name="Пароль").fill(os.getenv("PASSWORD"))
        page.get_by_role("button", name="Войти").click()

    with allure.step("Проверка корректной авторизации тестового тренера"):
        page.wait_for_url('https://pokemonbattle.ru/')
        expect(page.get_by_role("link", name="ID 64411 логотип")).to_be_visible()
        
    return page.context.storage_state()