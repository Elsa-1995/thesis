import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AviasalesPage:
    """Page Object для главной страницы Aviasales."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть главную страницу")
    def open(self):
        """Открывает главную страницу Aviasales."""
        self.driver.get("https://www.aviasales.ru")
        # Ждем загрузки страницы
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    @allure.step("Получить заголовок страницы")
    def get_title(self):
        """Возвращает заголовок страницы."""
        return self.driver.title

    @allure.step("Получить поле 'Откуда'")
    def get_origin_field(self):
        """Находит поле ввода для города отправления."""
        # Пробуем разные селекторы
        selectors = [
            "input[placeholder*='Откуда']",
            "input[placeholder*='откуда']",
            "[data-test-id='origin']",
            "#origin",
            ".origin-field input"
        ]
        for selector in selectors:
            try:
                return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            except:
                continue
        raise Exception("Не удалось найти поле 'Откуда'")

    @allure.step("Получить поле 'Куда'")
    def get_destination_field(self):
        """Находит поле ввода для города назначения."""
        # Пробуем разные селекторы
        selectors = [
            "input[placeholder*='Куда']",
            "input[placeholder*='куда']",
            "[data-test-id='destination']",
            "#destination",
            ".destination-field input"
        ]
        for selector in selectors:
            try:
                return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            except:
                continue
        raise Exception("Не удалось найти поле 'Куда'")

    @allure.step("Заполнить поле 'Откуда'")
    def set_origin(self, city):
        """Заполняет поле 'Откуда' указанным городом."""
        field = self.get_origin_field()
        field.clear()
        field.send_keys(city)

    @allure.step("Заполнить поле 'Куда'")
    def set_destination(self, city):
        """Заполняет поле 'Куда' указанным городом."""
        field = self.get_destination_field()
        field.clear()
        field.send_keys(city)

    @allure.step("Нажать поиск")
    def search(self):
        """Нажимает кнопку поиска билетов."""
        # Ищем кнопку поиска разными способами
        selectors = [
            "button[type='submit']",
            "button:contains('Найти')",
            ".search-button",
            "[data-test-id='search-button']",
            "button.search-btn"
        ]

        for selector in selectors:
            try:
                buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        self.wait.until(EC.element_to_be_clickable(button))
                        button.click()
                        return
            except:
                continue

        # Если не нашли, пробуем найти по тексту
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if button.is_displayed() and button.is_enabled():
                text = button.text.lower()
                if "найти" in text or "search" in text:
                    self.wait.until(EC.element_to_be_clickable(button))
                    button.click()
                    return

    @allure.step("Получить URL")
    def get_url(self):
        """Возвращает текущий URL страницы."""
        return self.driver.current_url

    @allure.step("Найти футер")
    def find_footer(self):
        """Находит футер сайта."""
        selectors = [
            "footer",
            ".footer",
            "[data-test-id='footer']",
            "div.footer"
        ]
        for selector in selectors:
            try:
                return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            except:
                continue
        raise Exception("Не удалось найти футер")

    @allure.step("Получить логотип")
    def find_logo(self):
        """Находит логотип сайта."""
        selectors = [
            "a[href='/']",
            ".logo",
            "[data-test-id='logo']",
            "img[alt*='Aviasales']",
            "img[alt*='логотип']"
        ]
        for selector in selectors:
            try:
                return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            except:
                continue
        return None
