import os
import re
import allure
from playwright.sync_api import expect
from pages.main_page import MainPage
from pages.payments_page import PaymentsPage
from pages.premium_page import PremiumPage
from pages.trainer_profile_page import TrainerProfilePage
from pages.secure_payment_page import SecurePaymentPage


@allure.suite("Тесты взаимодействия с тренером")
class TestTrainerUi:

    @allure.title("Профиль тренера: навигация")
    def test_navigation_to_trainer_profile(self, page):
        main_page = MainPage(page)
        profile_page = TrainerProfilePage(page)

        with allure.step("Переход на главную страницу"):
            main_page.open_page()
            main_page.check_page_is_main_page()

        with allure.step("Проверка корректной авторизации тестового тренера"):
            expect(main_page.trainer_badge).to_be_visible()

        with allure.step("Переход в профиль тренера"):
            main_page.trainer_badge.click()
            profile_page.check_page_is_profile_page()


    @allure.title("Переход со страницы тренера в раздел покупки Премиума")
    def test_navigation_to_premium_page(self, page):
        main_page = MainPage(page)
        profile_page = TrainerProfilePage(page)
        premium_page = PremiumPage(page)

        with allure.step("Переход в профиль тренера"):
            main_page.open_page()
            main_page.check_page_is_main_page()
            main_page.trainer_badge.click()
            profile_page.check_page_is_profile_page()

        with allure.step("Переход на страницу покупки премиума"):
            profile_page.premium_button.click()
            premium_page.element_visible(premium_page.heading)


    @allure.title("Проверка активности ачивки")
    def test_beginning_achievement_is_active(self, page):
        main_page = MainPage(page)
        profile_page = TrainerProfilePage(page)

        with allure.step("Переход в профиль тренера"):
            main_page.open_page()
            main_page.check_page_is_main_page()
            main_page.trainer_badge.click()
            profile_page.check_page_is_profile_page()

        with allure.step("Проверка состояния достижения"):
            expect(profile_page.beginning_achievement).to_have_class(re.compile(r"active"))

    @allure.title("Покупка премиума")
    def test_premium_purchase_success(self, page, check_and_cancel_premium):
        premium_page = PremiumPage(page)
        payments_page = PaymentsPage(page)
        secure_payment_page = SecurePaymentPage(page)
        test_days = "15"

        with allure.step("Переход на страницу покупки премиума"):
            premium_page.open_page()
            premium_page.check_page_is_premium_page()
            premium_page.element_visible(premium_page.heading)

        with allure.step("Заполнение поля Количество дней"):
            premium_page.premium_days_input.fill(test_days)

        with allure.step("Переход к оплате премиума с выбранным кол-вом дней"):
            premium_page.go_to_payment_button.click()
            payments_page.check_page_is_payments_page()

        with (allure.step("Заполнение формы оплаты валидными данными")):
            payments_page.fill_card_details()
            expect(payments_page.pay_button).to_have_class("style_1_base_button_payment")

        with allure.step("Нажатие кнопки Оплатить и переход на страницу ввода кода подтверждения"):
            payments_page.submit_payment()
            secure_payment_page.check_page_is_secure_payment_page()

        with allure.step("Ввод кода подтверждения"):
            secure_payment_page.confirm_payment()
            secure_payment_page.check_page_is_success_payment_page()

        with allure.step("Проверка начисленных дней премиума"):
            secure_payment_page.open_receipt_button.click()
            secure_payment_page.element_visible(page.get_by_text(f"Pokemon Premium: {test_days} дней"))

    @allure.title("Отмена премиума")
    def test_cancel_premium_success(self, page):
        premium_page = PremiumPage(page)
        with allure.step("Переход на страницу премиума"):
            premium_page.open_page()
            premium_page.check_page_is_premium_page()

        with allure.step("Нажатие кнопки отмены премиума"):
            premium_page.cancel_premium()
            premium_page.element_visible(premium_page.cancel_premium_dialogue)

        with allure.step(("Подтверждение отмены подписки")):
            premium_page.confirm_cancel_premium()
            premium_page.element_visible(premium_page.cancel_premium_success_notify)