import allure
import pytest
import requests
from config import config


@allure.epic("API Тесты Aviasales")
class TestAPI:
    """5 API-тестов для проверки работы API Aviasales."""

    @allure.title("1. Поиск билетов Москва → Санкт-Петербург (в одну сторону)")
    @allure.story("Базовый функционал API")
    @pytest.mark.api
    def test_search_one_way(self, api_client):
        """Тест проверяет поиск билетов в одну сторону.

        Параметры запроса:
        - origin: MOW (Москва)
        - destination: LED (Санкт-Петербург)
        - departure_at: 2026-02-01 (конкретная дата)

        Ожидается успешный ответ с данными о билетах.
        """
        with allure.step("Отправить запрос на поиск билетов"):
            response = api_client.search_one_way(
                origin=config.ORIGIN_CITY,  # Москва
                destination=config.DESTINATION_CITY,  # Санкт-Петербург
                departure_at=config.DEPARTURE_DATE  # 1 февраля 2026
            )

        with allure.step("Проверить, что запрос выполнен успешно"):
            # API возвращает success: true при успешном выполнении
            assert response.get("success") == True, \
                f"Запрос не выполнен успешно. Ответ: {response}"

        with allure.step("Проверить структуру ответа"):
            # В ответе должны быть поля data и currency
            assert "data" in response, "В ответе нет данных о билетах"
            assert "currency" in response, "В ответе не указана валюта"

    @allure.title("2. Поиск билетов Москва → СПб → Москва (туда-обратно)")
    @allure.story("Расширенный функционал API")
    @pytest.mark.api
    def test_search_round_trip(self, api_client):
        """Тест проверяет поиск билетов туда-обратно.

        Параметры запроса:
        - origin: MOW (Москва)
        - destination: LED (Санкт-Петербург)
        - departure_at: 2026-02-01 (дата вылета)
        - return_at: 2026-02-03 (дата возвращения)
        """
        with allure.step("Отправить запрос на поиск билетов туда-обратно"):
            response = api_client.search_round_trip(
                origin=config.ORIGIN_CITY,
                destination=config.DESTINATION_CITY,
                departure_at=config.DEPARTURE_DATE,
                return_at=config.RETURN_DATE
            )

        with allure.step("Проверить успешность выполнения"):
            assert response.get("success") == True

        with allure.step("Проверить формат данных"):
            # Данные должны быть в виде списка
            data = response.get("data", [])
            assert isinstance(data, list), "Данные должны быть списком"

            # Если есть данные, проверяем их структуру
            if len(data) > 0:
                first_ticket = data[0]
                assert "price" in first_ticket, "В билете нет цены"
                assert "departure_at" in first_ticket, "В билете нет даты вылета"

    @allure.title("3. Поиск билетов по месяцу (без конкретной даты)")
    @allure.story("Гибкие параметры поиска")
    @pytest.mark.api
    def test_search_by_month(self, api_client):
        """Тест проверяет поиск по месяцу без указания конкретного дня.

        Это полезно для поиска самых дешевых билетов в течение месяца.
        Параметр departure_at: "2026-02" (только год и месяц)
        """
        with allure.step("Отправить запрос с указанием только месяца"):
            response = api_client.search_one_way(
                origin=config.ORIGIN_CITY,
                destination=config.DESTINATION_CITY,
                departure_at=config.DEPARTURE_MONTH  # "2026-02" - только месяц
            )

        with allure.step("Проверить успешность выполнения"):
            assert response.get("success") == True

    @allure.title("4. Поиск билетов по кодам аэропортов (Домодедово → Утапао)")
    @allure.story("Работа с кодами аэропортов")
    @pytest.mark.api


    def test_search_with_airport_codes(self, api_client):
        """Тест проверяет поиск по кодам конкретных аэропортов.

        Вместо кодов городов (MOW, LED) используем коды аэропортов:
        - origin: DME (Москва Домодедово)
        - destination: UTP (Паттайя Утапао, Таиланд)

        Это проверяет, что API понимает разные типы кодов.
        """
        with allure.step("Отправить запрос с кодами аэропортов"):
            response = api_client.search_one_way(
                origin=config.ORIGIN_AIRPORT,  # DME - Домодедово
                destination=config.DESTINATION_AIRPORT,  # UTP - Утапао
                departure_at=config.DEPARTURE_DATE
            )

        with allure.step("Проверить успешность выполнения"):
            # Запрос должен выполниться успешно
            # Может не быть данных о билетах, но API должен ответить
            assert response.get("success") == True


    @allure.title("5. Поиск с ограничением количества результатов")
    @allure.story("Пагинация и ограничения")
    @pytest.mark.api
    def test_search_with_limit(self):
        """Тест проверяет работу параметра limit.

        Параметр limit=5 ограничивает количество возвращаемых результатов.
        Это важно для производительности и пагинации.
        """
        with allure.step("Отправить запрос с limit=5"):
            url = f"{config.API_BASE_URL}prices_for_dates"
            params = {
                "origin": config.ORIGIN_CITY,
                "destination": config.DESTINATION_CITY,
                "departure_at": config.DEPARTURE_DATE,
                "limit": 5,  # Ограничиваем 5 результатами
                "token": config.API_TOKEN
            }

            # Отправляем запрос напрямую, так как в api_client нет параметра limit
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

        with allure.step("Проверить успешность выполнения"):
            assert data.get("success") == True

        with allure.step("Проверить количество результатов"):
            results = data.get("data", [])
            # API может вернуть меньше результатов, если их мало
            # Но никогда не должен вернуть больше, чем limit
            assert len(results) <= 5, \
                f"Получено {len(results)} результатов, но limit=5"
