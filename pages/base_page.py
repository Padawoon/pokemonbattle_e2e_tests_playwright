from playwright.sync_api import Page, Locator, expect


class BasePage:
    BASE_URL = "https://pokemonbattle.ru"

    # инициализатор дефолтных атрибутов объекта класса
    def __init__(self, page: Page, timeout: int = 5000):
        self.page = page
        self.timeout = timeout

    # метод перехода на страницу, принимает в себя урл в виде стринги
    def open(self, url: str):
        self.page.goto(url)

    # метод проверяет, что элемент виден на странице
    def element_visible(self, locator: Locator):
        expect(locator).to_be_visible(timeout=self.timeout)

    # метод проверяет, что элемент содержит конкретный текст
    def element_has_text(self, locator: Locator, text: str):
        expect(locator).to_have_text(text, timeout=self.timeout)

    # метод проверяет, что в содержащемся в нём тексте есть запрошенный текст
    def element_contain_text(self, locator: Locator, text: str):
        expect(locator).to_contain_text(text, timeout=self.timeout)

    def element_is_clickable(self, locator: Locator):
        expect(locator).to_be_enabled()