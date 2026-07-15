import os
import re
import allure
from playwright.sync_api import expect
from pytest_playwright.pytest_playwright import page


@allure.suite("Тесты взаимодействия с тренером")
class TestTrainerUi:

    @allure.title("Переход в профиль тренера")
    def test_navigation_to_trainer_profile(self, page):
        with allure.step("Переход на главную страницу"):
            page.goto("https://pokemonbattle.ru")

        with allure.step("Проверка корректной авторизации тестового тренера"):
            expect(page.get_by_role("link", name="ID 64411 логотип")).to_be_visible()

        with allure.step("Переход в профиль тренера"):
            page.get_by_role("link", name="ID 64411 логотип").click()
            expect(page.get_by_text("ID тренера64411")).to_be_visible()


    @allure.title("Переход со страницы тренера в раздел покупки Премиума")
    def test_navigation_to_premium_page(self, page):
        with allure.step("Переход в профиль тренера"):
            page.goto("https://pokemonbattle.ru")
            page.get_by_role("link", name="ID 64411 логотип").click()
            expect(page.get_by_text("ID тренера64411")).to_be_visible()

        with allure.step("Переход на страницу покупки премиума"):
            page.get_by_text("Pokemon Premium").click()
            expect(page.get_by_role("heading", name="Pokemon Premium")).to_be_visible()


    @allure.title("Проверка активности ачивки")
    def test_beginning_achievement_is_active(self, page):
        with allure.step("Переход в профиль тренера"):
            page.goto("https://pokemonbattle.ru")
            page.get_by_role("link", name="ID 64411 логотип").click()
            expect(page.get_by_text("ID тренера64411")).to_be_visible()

        with allure.step("Проверка состояния достижения"):
            expect(page.locator("#beginning")).to_have_class(re.compile(r"active"))

    @allure.title("Покупка премиума")
    def test_premium_purchase_success(self, page, check_and_cancel_premium):
        with allure.step("Переход на страницу покупки премиума"):
            test_days = "15"
            page.goto("https://pokemonbattle.ru/premium")
            expect(page.get_by_role("heading", name="Pokemon Premium")).to_be_visible()

        with allure.step("Заполнение поля Количество дней"):
            page.locator("input[name='day']").fill(test_days)

        with allure.step("Переход к оплате премиума с выбранным кол-вом дней"):
            page.get_by_role("button", name="Перейти к оплате").click()
            page.wait_for_url("https://pokemonbattle.ru/payment/*")
            expect(page.get_by_role("button", name="Оплатить")).to_be_visible()

        with (allure.step("Заполнение формы оплаты валидными данными")):
            page.get_by_role("textbox", name="0000 0000 0000 0000").fill(os.getenv("VISA"))
            page.get_by_role("textbox", name="00/00").fill(os.getenv("DUE_DATE"))
            page.get_by_placeholder("000", exact=True).fill(os.getenv("SUCCESS_CVV"))
            page.get_by_placeholder("GERMAN DOLNIKOV").press_sequentially(os.getenv("CARD_NAME"), delay=10)

        with allure.step("Нажатие кнопки Оплатить и переход на страницу ввода кода подтверждения"):
            expect(page.get_by_role("button", name="Оплатить")).to_have_class("style_1_base_button_payment")
            page.get_by_role("button", name="Оплатить").click()
            page.wait_for_url("https://pokemonbattle.ru/payment_3ds")

        with allure.step("Ввод кода подтверждения"):
            page.get_by_role("textbox").fill(os.getenv("SECURE_CODE"))
            page.get_by_role("button", name="Оплатить").click()
            expect(page.get_by_text("Покупка прошла успешно")).to_be_visible()

        with allure.step("Проверка начисленных дней премиума"):
            page.locator("button.payment_receipt_open_button_icon").click()
            expect(page.get_by_text("Pokemon Premium: 15 дней")).to_be_visible()

    @allure.title("Отмена премиума")
    def test_cancel_premium_success(self, page):
        with allure.step("Переход на страницу премиума"):
            page.goto("https://pokemonbattle.ru/premium")
            expect(page.get_by_role("heading", name="Pokemon Premium")).to_be_visible()

        with allure.step("Нажатие кнопки отмены премиума"):
            page.locator("#cancel-premium").click()
            expect(page.get_by_text("Вы уверены, что хотите отменить подписку?", exact=True)).to_be_visible()

        with allure.step(("Подтверждение отмены подписки")):
            page.locator("#cancel-go-premium").click()
            expect(page.get_by_text("Вы отменили подписку :(", exact=True)).to_be_visible()