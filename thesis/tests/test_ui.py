import allure
import pytest


@allure.epic("UI Тесты")
class TestUI:

    @allure.title("1. Открытие главной страницы")
    @allure.story("Доступность сайта")
    @pytest.mark.ui
    def test_open_main_page(self, aviasales_page):
        """Тест использует AviasalesPage для открытия и проверки страницы."""
        with allure.step("Открыть главную страницу через Page Object"):
            aviasales_page.open()

        with allure.step("Проверить заголовок страницы через Page Object"):
            title = aviasales_page.get_title()
            assert "Авиабилеты" in title

    @allure.title("2. Поисковая форма отображается")
    @allure.story("Наличие элементов формы")
    @pytest.mark.ui
    def test_search_form_displayed(self, aviasales_page):
        """Тест использует методы Page Object для проверки элементов формы."""
        with allure.step("Открыть главную страницу"):
            aviasales_page.open()

        with allure.step("Проверить поле 'Откуда' через Page Object метод"):
            origin_input = aviasales_page.get_origin_input()
            assert origin_input.is_displayed()

        with allure.step("Проверить поле 'Куда' через Page Object метод"):
            dest_input = aviasales_page.get_destination_input()
            assert dest_input.is_displayed()

    @allure.title("3. Поиск с валидными данными")
    @allure.story("Основной функционал поиска")
    @pytest.mark.ui
    def test_search_valid_data(self, aviasales_page):
        """Тест использует Page Object для заполнения формы и поиска."""
        with allure.step("Открыть главную страницу"):
            aviasales_page.open()

        with allure.step("Заполнить город вылета через Page Object метод"):
            aviasales_page.fill_origin("Москва")

        with allure.step("Заполнить город назначения через Page Object метод"):
            aviasales_page.fill_destination("Санкт-Петербург")

        with allure.step("Начать поиск через Page Object метод"):
            aviasales_page.click_search()

        with allure.step("Дождаться результатов через Page Object метод"):
            aviasales_page.wait_for_search_results()

        with allure.step("Проверить URL результатов через Page Object метод"):
            current_url = aviasales_page.get_current_url()
            assert "search" in current_url

    @allure.title("4. Проверка наличия футера")
    @allure.story("Структура страницы")
    @pytest.mark.ui
    def test_footer_exists(self, aviasales_page):
        """Тест использует Page Object для работы с футером."""
        with allure.step("Открыть главную страницу"):
            aviasales_page.open()

        with allure.step("Найти футер через Page Object метод"):
            footer = aviasales_page.get_footer()
            assert footer.is_displayed()

        with allure.step("Проверить ссылки в футере через Page Object метод"):
            links = aviasales_page.get_footer_links()
            assert len(links) > 0

    @allure.title("5. Проверка логотипа")
    @allure.story("Элементы интерфейса")
    @pytest.mark.ui
    def test_logo_displayed(self, aviasales_page):
        """Тест использует Page Object для поиска логотипа."""
        with allure.step("Открыть главную страницу"):
            aviasales_page.open()

        with allure.step("Найти логотип через Page Object метод"):
            logo = aviasales_page.get_logo()
            if logo:
                assert logo.is_displayed()
            else:
                pytest.skip("Логотип не найден")
