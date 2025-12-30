import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # URL сайта для UI тестов
    BASE_URL = "https://www.aviasales.ru"

    # URL API из документации Travelpayouts
    API_BASE_URL = "https://api.travelpayouts.com/aviasales/v3/"
    API_TOKEN = os.getenv("API_TOKEN")

    # Тестовые данные (взяты из задания курсовой)
    # IATA-коды городов:
    # MOW = Москва (все аэропорты)
    # LED = Санкт-Петербург (Пулково)
    # DME = Москва Домодедово (конкретный аэропорт)
    # UTP = Паттайя Утапао (для теста аэропортов)
    ORIGIN_CITY = "MOW"
    DESTINATION_CITY = "LED"
    ORIGIN_AIRPORT = "DME"
    DESTINATION_AIRPORT = "UTP"

    # Тестовые даты (будущие даты для стабильности тестов)
    DEPARTURE_DATE = "2026-02-01"  # 1 февраля 2026
    RETURN_DATE = "2026-02-03"  # 3 февраля 2026
    DEPARTURE_MONTH = "2026-02"  # Февраль 2026 (только месяц)


config = Config()