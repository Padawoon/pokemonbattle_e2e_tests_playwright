# Pokemon Battle — UI-автотесты на Playwright + Pytest

Учебный проект по автоматизации тестирования веб-приложения [«Битва Покемонов»](https://pokemonbattle.ru) — тренажёра для QA-инженеров. Тесты написаны во время прохождения курса по автоматизации на Python.

Проект покрывает:

- **E2E-сценарии**: авторизация, навигация по профилю тренера, покупка и отмена подписки Pokemon Premium (включая оплату картой и подтверждение 3DS-кодом);
- **скриншот-тесты**: сравнение вёрстки ключевых форм и блоков с эталонными снимками.

## Стек

| Инструмент | Для чего используется |
|---|---|
| [Python 3.12+](https://www.python.org/) | Язык тестов (в коде есть f-строки с вложенными кавычками одного типа, а они работают только с 3.12) |
| [Pytest](https://docs.pytest.org/) | Тестовый раннер, фикстуры, параметризация |
| [Playwright](https://playwright.dev/python/) + [pytest-playwright](https://pypi.org/project/pytest-playwright/) | Управление браузером, локаторы, web-first ассерты `expect` |
| [pytest-playwright-snapshot](https://pypi.org/project/pytest-playwright-snapshot/) | Скриншот-тестирование через фикстуру `assert_snapshot` (сравнение выполняется через `pixelmatch`) |
| [pytest-order](https://pypi.org/project/pytest-order/) | Управление порядком запуска тестов (`--order-scope=module`) |
| [pytest-base-url](https://pypi.org/project/pytest-base-url/) | Базовый URL для тестов |
| [Allure](https://allurereport.org/docs/pytest/) (`allure-pytest`) | Отчёты: шаги `allure.step`, заголовки, сьюты, теги |
| [Requests](https://requests.readthedocs.io/) | API-вызовы для подготовки тестовых данных |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Загрузка учётных данных и тестовых данных из `.env` |

## Структура проекта

```
.
├── config/
│   └── api_config.py              # базовые URL API (api.pokemonbattle.ru, lavka.pokemonbattle.ru)
├── fixtures/
│   ├── api_fixtures.py            # API-сессия с trainer_token, сброс премиума до и после тестов
│   ├── auth_context_fixtures.py   # авторизация один раз за сессию, переиспользование storage_state
│   └── ui_fixtures.py             # загрузка .env, атрибут data-id для get_by_test_id
├── helpers/
│   └── auth_helper.py             # логин через UI, возвращает storage_state
├── pages/                         # Page Object Model
│   ├── base_page.py               # базовый класс: открытие страницы, общие проверки
│   ├── login_page.py
│   ├── main_page.py
│   ├── trainer_profile_page.py
│   ├── premium_page.py
│   ├── payments_page.py
│   └── secure_payment_page.py     # страница ввода 3DS-кода и успешной оплаты
├── tests/
│   ├── e2e/
│   │   ├── test_login.py          # авторизация с нуля (без сохранённой сессии)
│   │   └── authorized/            # тесты под авторизованным тренером
│   │       ├── conftest.py
│   │       └── test_pokemonbattle_e2e.py
│   └── screenshot/
│       ├── conftest.py
│       ├── test_screenshot_buy_premium_form.py
│       ├── test_screenshot_card_details_form.py
│       ├── test_screenshot_trainer_profile_page.py
│       └── __snapshots__/         # эталонные скриншоты (chromium/win32)
├── conftest.py                    # подключение плагинов с фикстурами
├── pytest.ini
└── requirements.txt
```

## Архитектура и подходы

- **Page Object Model.** Каждая страница описана классом, унаследованным от `BasePage`. Локаторы оформлены как `@property`, действия и проверки — как методы (`open_page()`, `check_page_is_*_page()`, `fill_card_details()` и т. д.).
- **Авторизация один раз за сессию.** Фикстура `auth_state` логинится через UI, кэширует `storage_state` (куки и localStorage), а переопределённая `browser_context_args` подставляет его в каждый новый контекст вместе с вьюпортом 1920×1080. Поэтому тесты в `authorized/` и `screenshot/` стартуют уже авторизованными.
- **Подготовка данных через API.** Перед тестом покупки фикстура `check_and_cancel_premium` проверяет через `GET /v2/me`, есть ли у тренера премиум, и при необходимости отменяет его через `POST /cancel_premium`. После тестов то же самое повторяется, чтобы тренер остался в исходном состоянии.
- **Пользовательские локаторы.** В основном `get_by_role` / `get_by_text` / `get_by_placeholder`, CSS и XPath — там, где без них не обойтись. Атрибут для `get_by_test_id` переопределён на `data-id`.
- **Стабильные скриншоты.** Динамические данные (покеболы, уровень, ачивки) закрываются маской `mask=[...]` с `mask_color`. Перед снимком тест дожидается нужного состояния элемента через `expect`.
- **Параметризация.** Скриншоты формы премиума проверяются для разных диапазонов дней (скидочные пороги < 30, 30–180, 180–365, > 365), форма оплаты — для невалидного номера карты и срока действия.
- **Allure-разметка.** Шаги теста описаны на русском через `allure.step`, используются `@allure.title`, `@allure.suite`, `@allure.tag`.

## Покрытые сценарии

### E2E

| Тест | Что проверяет |
|---|---|
| `test_login` | Редирект неавторизованного пользователя на `/login`, вход по email и паролю, отображение бейджа тренера |
| `test_navigation_to_trainer_profile` | Переход с главной страницы в профиль тренера |
| `test_navigation_to_premium_page` | Переход из профиля на страницу Pokemon Premium |
| `test_beginning_achievement_is_active` | Ачивка «Начало» в профиле активна |
| `test_premium_purchase_success` | Полный флоу покупки премиума: выбор количества дней → форма карты → 3DS-код → успешная оплата → проверка чека |
| `test_cancel_premium_success` | Отмена подписки с подтверждением в диалоге |

### Скриншот-тесты

| Тест | Эталоны |
|---|---|
| `test_buy_premium_visual` | `buy_premium_form_*.png` — форма покупки для четырёх диапазонов дней |
| `test_empty_card_details_form_empty_visual` | `empty_card_details_form.png` |
| `test_filled_card_details_form_visual` | `filled_card_details_form.png` |
| `test_invalid_invalid_inputs_visual` | `invalid_card_number.png`, `invalid_expiry.png` |
| `test_trainer_stats_visual` | `trainer_stats.png` — блок характеристик тренера с замаскированными динамическими значениями |

## Установка

```bash
git clone <url-репозитория>
cd pokemonbattle_e2e_tests_playwright

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium
```

> `requirements.txt` сохранён в кодировке UTF-16 (так получается при `pip freeze > requirements.txt` в PowerShell). Если `pip` не может его прочитать, пересохрани файл в UTF-8.

## Переменные окружения

Тестам нужен файл `.env` в корне проекта со следующими переменными:

```dotenv
# тренер
LOGIN=               # email тестового тренера
PASSWORD=            # пароль
USER_TRAINER_TOKEN=  # API-токен тренера (заголовок trainer_token)
TRAINER_ID=          # ID тренера

# тестовые карты
VISA=                # номер карты для оплаты
MASTERCARD=
DUE_DATE=            # срок действия, формат MM/YY
SUCCESS_CVV=
FAIL_CVV=
CARD_NAME=           # имя держателя карты
SECURE_CODE=         # 3DS-код подтверждения
```

## Запуск тестов

```bash
# все тесты
pytest

# только E2E
pytest tests/e2e

# только скриншот-тесты
pytest tests/screenshot

# с видимым браузером и замедлением
pytest --headed --slowmo 300

# обновить эталонные скриншоты
pytest tests/screenshot --update-snapshots
```

Эталонные скриншоты лежат в `tests/screenshot/__snapshots__/chromium/win32/`. Они сняты в Chromium на Windows, поэтому на другой ОС или в другом браузере (например, в Linux CI) из-за разного рендеринга шрифтов эталоны нужно будет снять заново.

## Allure-отчёт

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

Для `allure serve` нужен установленный [Allure CLI](https://allurereport.org/docs/install/).
