import pytest
from dotenv import load_dotenv
from helpers.auth_helper import login


# подгрузка переменных из .env
@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

# задаём селектору get_by_test_id поиск по data-id (используется в тестовом проекте)
@pytest.fixture(scope='session', autouse=True)
def _set_test_id_attribute(playwright):
    playwright.selectors.set_test_id_attribute('data-id')


# фикстура один раз за сессию авторизуется и сохраняет куки в память
_auth_state_cache = None

@pytest.fixture(scope="session")
def auth_state(browser, load_env):
    global _auth_state_cache
    if _auth_state_cache is None:
        # запускаем браузер в headless-режиме для быстрой авторизации
        context = browser.new_context()
        page = context.new_page()

        # вызываем хелпер, который возвращает state
        _auth_state_cache = login(page)

        context.close()
    return _auth_state_cache

# фикстура, чтобы каждый тест стартовал с сохраненными куками и нормальным вьюпортом
@pytest.fixture()
def browser_context_args(browser_context_args, auth_state):
    return {
        **browser_context_args,
        "storage_state": auth_state,
        "viewport": {
            "width": 1920,
            "height": 1080
        }
    }