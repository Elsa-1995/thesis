import allure
import pytest
import requests
from config import config


@allure.epic("API Тесты")
@allure.feature("Проверка API Aviasales")
class TestAPI:
    """5 API тестов для проверки работы API Aviasales."""

    @allure.title("Тест 1: Поиск перелёта в одну сторону")
    @allure.story("Базовый функционал API")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_search_one_way(self, api_client):
        """
        Поиск билетов в одну сторону (Москва → Санкт-Петербург).

        Проверяет:
        1. Успешность выполнения запроса
        2. Структуру ответа
        """
        with allure.step("Отправить запрос на поиск билетов MOW → LED"):
            response = api_client.search_one_way(
                origin="MOW",
                destination="LED",
                departure_at="2025-09-01"
            )

        with allure.step("Проверить, что запрос выполнен успешно (success: true)"):
            assert response.get("success") == True, \
                f"Запрос не выполнен успешно. Ответ: {response}"

        with allure.step("Проверить структуру ответа (должны быть поля data и currency)"):
            assert "data" in response, "В ответе отсутствует поле 'data'"
            assert "currency" in response, "В ответе отсутствует поле 'currency'"

    @allure.title("Тест 2: Поиск перелёта туда-обратно")
    @allure.story("Расширенный функционал API")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_search_round_trip(self, api_client):
        """
        Поиск билетов туда-обратно (Москва → СПб → Москва).

        Проверяет:
        1. Успешность выполнения запроса
        2. Наличие данных в ответе
        """
        with allure.step("Отправить запрос на поиск билетов туда-обратно"):
            response = api_client.search_round_trip(
                origin="MOW",
                destination="LED",
                departure_at="2025-09-01",
                return_at="2025-09-03"
            )

        with allure.step("Проверить успешность выполнения запроса"):
            assert response.get("success") == True

        with allure.step("Проверить, что данные пришли в формате списка"):
            data = response.get("data", [])
            assert isinstance(data, list), "Данные должны быть списком"

    @allure.title("Тест 3: Поиск по месяцу (без конкретной даты)")
    @allure.story("Гибкие параметры поиска")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_search_by_month(self, api_client):
        """
        Поиск билетов по месяцу без указания конкретного дня.

        Это полезно для поиска самых дешевых билетов в течение месяца.
        """
        with allure.step("Отправить запрос с указанием только месяца"):
            response = api_client.search_one_way(
                origin="MOW",
                destination="LED",
                departure_at="2025-09"  # Только год и месяц
            )

        with allure.step("Проверить успешность выполнения запроса"):
            assert response.get("success") == True

    @allure.title("Тест 4: Поиск по кодам аэропортов (Домодедово → Утапао)")
    @allure.story("Разные типы кодов")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_search_with_airport_codes(self, api_client):
        """
        Поиск по кодам конкретных аэропортов вместо кодов городов.

        Проверяет, что API понимает разные типы кодов:
        - DME = Москва Домодедово (аэропорт)
        - UTP = Паттайя Утапао (аэропорт, Таиланд)
        """
        with allure.step("Отправить запрос с кодами аэропортов"):
            response = api_client.search_one_way(
                origin="DME",
                destination="UTP",
                departure_at="2025-09-01"
            )

        with allure.step("Проверить успешность выполнения запроса"):
        # Запрос должен выполниться успешно
        # Может не быть данных о билетах, но API должен ответить
        assert response.get("success") == True

    @allure.title("Тест 5: Поиск с ограничением количества результатов")
    @allure.story("Пагинация и ограничения")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_search_with_limit(self):
        """
        Поиск с ограничением количества возвращаемых результатов.

        Проверяет работу параметра limit=5.
        Это важно для производительности и пагинации.
        """
        with allure.step("Отправить запрос с limit=5"):
            url = f"{config.API_BASE_URL}prices_for_dates"
            params = {
                "origin": "MOW",
                "destination": "LED",
                "departure_at": "2025-09-01",
                "limit": 5,  # Ограничиваем 5 результатами
                "token": config.API_TOKEN
            }

            # Отправляем запрос напрямую, так как в api_client нет параметра limit
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

        with allure.step("Проверить успешность выполнения запроса"):
            assert data.get("success") == True

        with allure.step("Проверить количество результатов (не более 5)"):
            results = data.get("data", [])
            # API может вернуть меньше результатов, если их мало
            # Но никогда не должен вернуть больше, чем limit
            assert len(results) <= 5, \
                f"Получено {len(results)} результатов, но limit=5"