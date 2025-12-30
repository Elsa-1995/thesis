import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional


class AviasalesPage:
    """Page Object для главной страницы Aviasales."""

    # Локаторы элементов
    ORIGIN_INPUT = (By.CSS_SELECTOR, "[data-test-id='origin-autocomplete-field']")
    DESTINATION_INPUT = (By.CSS_SELECTOR, "[data-test-id='destination-autocomplete-field']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "[data-test-id='form-submit']")
    FOOTER = (By.TAG_NAME, "footer")
    LOGO = (By.CSS_SELECTOR, "[data-test-id='logo'], .logo, [class*='logo']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть главную страницу")
    def open(self) -> None:
        self.driver.get("https://www.aviasales.ru")

    @allure.step("Получить заголовок страницы")
    def get_title(self) -> str:
        return self.driver.title

    @allure.step("Найти поле 'Откуда'")
    def get_origin_input(self) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(self.ORIGIN_INPUT))

    @allure.step("Найти поле 'Куда'")
    def get_destination_input(self) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(self.DESTINATION_INPUT))

    @allure.step("Заполнить поле 'Откуда' значением {city}")
    def fill_origin(self, city: str) -> None:
        field = self.get_origin_input()
        field.clear()
        field.send_keys(city)

    @allure.step("Заполнить поле 'Куда' значением {city}")
    def fill_destination(self, city: str) -> None:
        field = self.get_destination_input()
        field.clear()
        field.send_keys(city)

    @allure.step("Нажать кнопку поиска")
    def click_search(self) -> None:
        button = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        button.click()

    @allure.step("Дождаться перехода на страницу результатов")
    def wait_for_search_results(self) -> None:
        self.wait.until(EC.url_contains("/search"))

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url

    @allure.step("Найти футер сайта")
    def get_footer(self) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(self.FOOTER))

    @allure.step("Найти логотип")
    def get_logo(self) -> Optional[WebElement]:
        try:
            return self.wait.until(EC.visibility_of_element_located(self.LOGO))
        except:
            return None

    @allure.step("Получить все ссылки в футере")
    def get_footer_links(self) -> list:
        footer = self.get_footer()
        return footer.find_elements(By.TAG_NAME, "a")