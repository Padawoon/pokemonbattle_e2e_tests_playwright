import pytest
from helpers.auth_helper import login

# фикстура один раз за сессию авторизуется и сохраняет куки в память
_auth_state_cache = None

@pytest.fixture(scope="session")
def auth_state(browser):
    global _auth_state_cache
    if _auth_state_cache is None:
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