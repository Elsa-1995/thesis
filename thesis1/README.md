Автоматизация тестирования Aviasales

Курсовой проект по автоматизации UI и API тестирования сайта Aviasales.

Структура проекта

coursework-automation/
├── pages/
│   └── aviasales_page.py
├── tests/
│   ├── test_ui.py
│   └── test_api.py
├── .gitignore
├── README.md
├── requirements.txt
├── .env
├── config.py
├── api_client.py
└── conftest.py

Требования

- Python 3.8 или выше
- Google Chrome (для UI тестов)
- Git

Быстрый старт

1. Клонирование и настройка

Клонировать репозиторий:
git clone <ваш-репозиторий>
cd coursework-automation

Создать виртуальное окружение:
python -m venv venv

Активировать окружение:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

Установить зависимости:
pip install -r requirements.txt

2. Настройка API токена

Создайте файл .env в корне проекта с содержимым:
API_TOKEN=ccdf2589d756718b9cd13d8854d2b89e

Запуск тестов

Все тесты (UI + API):
pytest

Только UI тесты (5 тестов):
pytest -m ui

Только API тесты (5 тестов):
pytest -m api

С подробным выводом:
pytest -v

С отчетом Allure:
pytest --alluredir=allure-results
allure serve allure-results

Из папки tests:
pytest tests/

Описание тестов

UI тесты (5 тестов в tests/test_ui.py)
Используют Page Object Pattern из pages/aviasales_page.py:

1. test_open_main_page - Открытие главной страницы Aviasales
2. test_search_form_displayed - Проверка отображения поисковой формы
3. test_simple_search - Поиск билетов с валидными данными
4. test_footer_exists - Проверка наличия и содержимого футера
5. test_logo_exists - Проверка отображения логотипа

API тесты (5 тестов в tests/test_api.py)
Используют TravelPayouts API:

1. test_search_one_way - Поиск перелёта в одну сторону
2. test_search_round_trip - Поиск перелёта туда-обратно
3. test_search_by_month - Поиск по месяцу (без указания дня)
4. test_search_with_airport_codes - Поиск по кодам аэропортов
5. test_search_with_limit - Поиск с лимитом результатов

Технологии

- Python 3.8+ - основной язык программирования
- Selenium WebDriver - автоматизация браузера
- Pytest - фреймворк для тестирования
- Requests - HTTP-запросы для API тестов
- Allure Framework - генерация отчетов
- Page Object Pattern - паттерн проектирования для UI тестов
- dotenv - управление переменными окружения

Описание файлов

pages/aviasales_page.py
Page Object Model для главной страницы Aviasales. Содержит локаторы и методы взаимодействия с элементами страницы.

tests/test_ui.py
5 UI тестов, использующих Page Object Pattern.

tests/test_api.py
5 API тестов для проверки функционала TravelPayouts API.

config.py
Конфигурация проекта: URL, токены API, тестовые данные.

api_client.py
Клиент для работы с API Aviasales. Инкапсулирует логику HTTP-запросов.

conftest.py
Фикстуры Pytest:
- driver - создание и завершение WebDriver
- aviasales_page - инициализация Page Object
- api_client - инициализация API клиента

requirements.txt
Зависимости проекта:
selenium>=4.15.0
requests>=2.31.0
pytest>=7.4.0
allure-pytest>=2.13.0
python-dotenv>=1.0.0
webdriver-manager>=4.0.0

.env
Файл с переменными окружения (не добавляется в git):
API_TOKEN=ваш_токен

Важные импорты

Для правильной работы убедитесь в корректности импортов:

В test_ui.py:
from pages.aviasales_page import AviasalesPage

В test_api.py:
from api_client import AviasalesAPI
from config import config

В conftest.py:
from pages.aviasales_page import AviasalesPage
from api_client import AviasalesAPI

Импорт config.py:
from config import config

Генерация отчетов

Проект поддерживает генерацию отчетов в формате Allure:

1. Установите Allure
2. Запустите тесты с генерацией данных:
   pytest --alluredir=allure-results
3. Откройте отчет:
   allure serve allure-results

Проверка проекта

Проект соответствует всем требованиям курсовой работы:
- 5 UI тестов с использованием Page Object
- 5 API тестов
- Чистая структура проекта с папками pages и tests
- Использование конфигурационных файлов
- Поддержка Allure отчетов
- Документация в README.md

