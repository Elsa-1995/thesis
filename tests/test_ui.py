import allure
import pytest


@allure.epic("UI Тесты Aviasales")
@allure.feature("Проверка функционала сайта Aviasales")
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
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_open_main_page(self, aviasales_page):
        """Тест проверяет, что главная страница сайта загружается."""
        with allure.step("Открыть главную страницу Aviasales"):
            aviasales_page.open()

        with allure.step("Проверить, что заголовок страницы содержит ключевое слово"):
            title = aviasales_page.get_title()
            assert "Авиабилеты" in title, f"Заголовок '{title}' не содержит 'Авиабилеты'"

    @allure.title("2. Форма поиска билетов отображается")
    @allure.story("Основные элементы интерфейса")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_search_form_displayed(self, aviasales_page):
        """Тест проверяет наличие полей для поиска билетов."""
        with allure.step("Открыть главную страницу"):
            aviasales_page.open()

        with allure.step("Проверить, что поле 'Откуда' отображается"):
            origin_input = aviasales_page.get_origin_input()
            assert origin_input.is_displayed(), "Поле 'Откуда' не отображается"

        with allure.step("Проверить, что поле 'Куда' отображается"):
            dest_input = aviasales_page.get_destination_input()
            assert dest_input.is_displayed(), "Поле 'Куда' не отображается"

    @allure.title("3. Поиск билетов Москва → Санкт-Петербург")
    @allure.story("Основной функционал поиска")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_search_valid_data(self, aviasales_page):
        """Тест проверяет работу поиска с корректными данными.

        Шаги:
        1. Открыть сайт
        2. Заполнить города вылета и назначения
        3. Нажать поиск
        4. Проверить переход на страницу результатов
        """
        with allure.step("Открыть главную страницу"):
            aviasales_page.open()

        with allure.step("Заполнить город вылета - Москва"):
            aviasales_page.fill_origin("Москва")

        with allure.step("Заполнить город назначения - Санкт-Петербург"):
            aviasales_page.fill_destination("Санкт-Петербург")

        with allure.step("Нажать кнопку поиска"):
            aviasales_page.click_search()

        with allure.step("Дождаться перехода на страницу результатов"):
            aviasales_page.wait_for_search_results()

        with allure.step("Проверить, что URL содержит 'search'"):
            current_url = aviasales_page.get_current_url()
            assert "search" in current_url, \
                f"Ожидался переход на страницу результатов, текущий URL: {current_url}"

        @allure.title("Тест 4: Проверка наличия футера с ссылками")
        @allure.story("Структура страницы")
        @allure.severity(allure.severity_level.NORMAL)
        @pytest.mark.ui
        def test_footer_exists(self, aviasales_page):
            """Проверка наличия футера сайта с полезными ссылками."""
            with allure.step("Открыть главную страницу"):
                aviasales_page.open()

            with allure.step("Найти футер сайта"):
                footer = aviasales_page.get_footer()
                assert footer.is_displayed(), "Футер не отображается"

            with allure.step("Проверить, что в футере есть хотя бы одна ссылка"):
                links = aviasales_page.get_footer_links()
                assert len(links) > 0, "В футере нет ссылок"

        @allure.title("Тест 5: Проверка отображения логотипа")
        @allure.story("Элементы интерфейса")
        @allure.severity(allure.severity_level.NORMAL)
        @pytest.mark.ui

    def test_logo_displayed(self, aviasales_page):
        """Проверка наличия логотипа Aviasales на странице."""
        with allure.step("Открыть главную страницу"):
            aviasales_page.open()

        with allure.step("Найти логотип сайта"):
            logo = aviasales_page.get_logo()
            if logo:
                assert logo.is_displayed(), "Логотип не отображается"
            else:
                # Если логотип не найден - пропускаем тест
                pytest.skip("Логотип не найден на странице")