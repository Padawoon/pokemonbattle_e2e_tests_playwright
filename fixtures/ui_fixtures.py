import pytest
from dotenv import load_dotenv


# подгрузка переменных из .env
@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

# задаём селектору get_by_test_id поиск по data-id (используется в тестовом проекте)
@pytest.fixture(scope='session', autouse=True)
def _set_test_id_attribute(playwright):
    playwright.selectors.set_test_id_attribute('data-id')
