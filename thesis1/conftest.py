import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    """Фикстура для инициализации WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Новый headless режим
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()


@pytest.fixture
def aviasales_page(driver):
    """Фикстура для создания Page Object."""
    from pages.aviasales_page import AviasalesPage
    return AviasalesPage(driver)


@pytest.fixture
def api_client():
    """Фикстура для создания клиента API."""
    from api_client import AviasalesAPI
    return AviasalesAPI()


def pytest_collection_modifyitems(items):
    """Автоматическая маркировка тестов."""
    for item in items:
        if "test_ui" in item.nodeid:
            item.add_marker(pytest.mark.ui)
        elif "test_api" in item.nodeid:
            item.add_marker(pytest.mark.api)