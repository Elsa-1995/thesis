import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import config


@allure.epic("UI Тесты Aviasales")
class TestUI:
    """5 UI-тестов для проверки основного функционала сайта Aviasales.

    Тесты проверяют:
    1. Доступность сайта
    2. Наличие основных элементов
    3. Работу поиска билетов
    4. Структуру страницы
    5. Ключевые элементы интерфейса
    """

    @allure.title("1. Главная страница доступна")
    @allure.story("Доступность сайта")
    @pytest.mark.ui
    def test_open_main_page(self, driver):
        """Тест проверяет, что главная страница сайта загружается."""
        # Открываем сайт
        driver.get(config.BASE_URL)

        # Проверяем, что заголовок содержит ключевое слово
        # Это подтверждает, что мы на правильном сайте
        assert "Авиабилеты" in driver.title

    @allure.title("2. Форма поиска билетов отображается")
    @allure.story("Основные элементы интерфейса")
    @pytest.mark.ui
    def test_search_form_displayed(self, driver):
        """Тест проверяет наличие полей для поиска билетов."""
        driver.get(config.BASE_URL)

        # Ищем поле "Откуда" по data-test-id атрибуту
        # Это стабильный локатор, который редко меняется
        origin_input = driver.find_element(
            By.CSS_SELECTOR,
            "[data-test-id='origin-autocomplete-field']"
        )
        assert origin_input.is_displayed(), "Поле 'Откуда' не отображается"

        # Ищем поле "Куда"
        dest_input = driver.find_element(
            By.CSS_SELECTOR,
            "[data-test-id='destination-autocomplete-field']"
        )
        assert dest_input.is_displayed(), "Поле 'Куда' не отображается"

    @allure.title("3. Поиск билетов Москва → Санкт-Петербург")
    @allure.story("Основной функционал поиска")
    @pytest.mark.ui
    def test_search_valid_data(self, driver):
        """Тест проверяет работу поиска с корректными данными.

        Шаги:
        1. Открыть сайт
        2. Заполнить города вылета и назначения
        3. Нажать поиск
        4. Проверить переход на страницу результатов
        """
        driver.get(config.BASE_URL)

        # Заполняем город вылета
        origin_field = driver.find_element(
            By.CSS_SELECTOR,
            "[data-test-id='origin-autocomplete-field']"
        )
        origin_field.clear()
        origin_field.send_keys("Москва")  # Город отправления

        # Заполняем город назначения
        dest_field = driver.find_element(
            By.CSS_SELECTOR,
            "[data-test-id='destination-autocomplete-field']"
        )
        dest_field.clear()
        dest_field.send_keys("Санкт-Петербург")  # Город назначения

        # Нажимаем кнопку поиска
        search_button = driver.find_element(
            By.CSS_SELECTOR,
            "[data-test-id='form-submit']"
        )
        search_button.click()

        # Ждем, пока URL изменится на страницу результатов
        # Максимальное время ожидания - 10 секунд
        WebDriverWait(driver, 10).until(
            EC.url_contains("/search")
        )

        # Проверяем, что мы на странице результатов
        assert "search" in driver.current_url, \
            f"Ожидался переход на страницу результатов, текущий URL: {driver.current_url}"

    @allure.title("4. Наличие футера с ссылками")
    @allure.story("Структура страницы")
    @pytest.mark.ui
    def test_footer_exists(self, driver):
        """Тест проверяет наличие футера сайта.

        Футер - важный элемент, содержащий ссылки на:
        - Помощь
        - Правила
        - Контакты
        - Документы
        """
        driver.get(config.BASE_URL)

        # Ищем футер по HTML тегу
        footer = driver.find_element(By.TAG_NAME, "footer")
        assert footer.is_displayed(), "Футер не отображается"
        # Проверяем, что в футере есть хотя бы одна ссылка
        links = footer.find_elements(By.TAG_NAME, "a")
        assert len(links) > 0, "В футере нет ссылок"

    @allure.title("5. Логотип сайта отображается")
    @allure.story("Брендинг и идентификация")
    @pytest.mark.ui
    def test_logo_displayed(self, driver):
        """Тест проверяет наличие логотипа Aviasales.

        Логотип - важный элемент брендинга, должен быть на всех страницах.
        """
        driver.get(config.BASE_URL)

        # Пытаемся найти логотип разными способами
        # 1. По data-test-id (если есть)
        try:
            logo = driver.find_element(By.CSS_SELECTOR, "[data-test-id='logo']")
            assert logo.is_displayed()
            return  # Если нашли - тест пройден
        except:
            pass  # Пробуем другой способ

        # 2. По классу, содержащему "logo"
        logos = driver.find_elements(
            By.CSS_SELECTOR,
            "[class*='logo'], [class*='Logo'], .logo"
        )

        assert len(logos) > 0, "Логотип не найден"
        assert logos[0].is_displayed(), "Логотип не отображается"