import requests
import allure
from config import config


class AviasalesAPI:
    """Клиент для работы с API Aviasales."""

    def search_one_way(self, origin: str, destination: str, departure_at: str) -> dict:
        url = f"{config.API_BASE_URL}prices_for_dates"
        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": departure_at,
            "token": config.API_TOKEN
        }

        with allure.step(f"API запрос: {params}"):
            response = requests.get(url, params=params, timeout=10)
            return response.json()

    def search_round_trip(self, origin: str, destination: str,
                          departure_at: str, return_at: str) -> dict:
        url = f"{config.API_BASE_URL}prices_for_dates"
        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": departure_at,
            "return_at": return_at,
            "token": config.API_TOKEN
        }

        with allure.step(f"API запрос: {params}"):
            response = requests.get(url, params=params, timeout=10)
            return response.json()