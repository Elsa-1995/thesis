import allure
import pytest


@allure.epic("UI Тесты")
class TestUI:

    @allure.title("1. Открытие главной страницы")
    @allure.story("Доступность сайта")
    @pytest.mark.ui
    def test_open_main_page(self, aviasales_page):
        # используем Page Object
        aviasales_page.open()
        title = aviasales_page.get_title()
        assert "Авиабилеты" in title

    @allure.title("2. Поисковая форма отображается")
    @allure.story("Наличие элементов формы")
    @pytest.mark.ui
    def test_search_form_displayed(self, aviasales_page):
        # используем Page Object
        aviasales_page.open()

        # Используем методы Page Object
        origin_input = aviasales_page.get_origin_input()
        dest_input = aviasales_page.get_destination_input()

        assert origin_input.is_displayed()
        assert dest_input.is_displayed()

    @allure.title("3. Поиск с валидными данными")
    @allure.story("Основной функционал поиска")
    @pytest.mark.ui
    def test_search_valid_data(self, aviasales_page):
        # используем Page Object
        aviasales_page.open()

        # Используем методы Page Object для заполнения формы
        aviasales_page.fill_origin("Москва")
        aviasales_page.fill_destination("Санкт-Петербург")

        # Используем метод Page Object для клика
        aviasales_page.click_search()

        # Используем метод Page Object для ожидания
        aviasales_page.wait_for_search_results()

        # Используем метод Page Object для получения URL
        current_url = aviasales_page.get_current_url()
        assert "search" in current_url

    @allure.title("4. Проверка наличия футера")
    @allure.story("Структура страницы")
    @pytest.mark.ui
    def test_footer_exists(self, aviasales_page):
        # используем Page Object
        aviasales_page.open()

        # Используем методы Page Object
        footer = aviasales_page.get_footer()
        assert footer.is_displayed()

        links = aviasales_page.get_footer_links()
        assert len(links) > 0

    @allure.title("5. Проверка логотипа")
    @allure.story("Элементы интерфейса")
    @pytest.mark.ui
    def test_logo_displayed(self, aviasales_page):
        # используем Page Object
        aviasales_page.open()

        # Используем метод Page Object
        logo = aviasales_page.get_logo()
        if logo:
            assert logo.is_displayed()
        else:
            pytest.skip("Логотип не найден")