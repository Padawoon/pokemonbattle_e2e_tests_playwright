import os
from http import HTTPStatus

import pytest
import requests

from config.api_config import BASE_URL, LAVKA_BASE_URL

# фикстура для передачи токена в API сессию
@pytest.fixture(scope="session")
def api_session():
    with requests.Session() as poke_session:
        poke_session.headers.update({"trainer_token": os.getenv("USER_TRAINER_TOKEN")})
        yield poke_session

# фикстура для проверки и отмены премиума у тренера перед тестами
@pytest.fixture(scope="session")
def check_and_cancel_premium(api_session):
    def _cancel_if_premium():
        response = api_session.get(BASE_URL + "/me")
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        if body.get("data")[0].get("is_premium"):
            prem_cancellation_response = api_session.post(LAVKA_BASE_URL + "/cancel_premium")
            assert prem_cancellation_response.status_code == HTTPStatus.OK

    _cancel_if_premium()
    yield
    _cancel_if_premium()