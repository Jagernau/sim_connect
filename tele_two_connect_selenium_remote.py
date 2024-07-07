from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config
import time
from selenium.webdriver.common.by import By
import random
from logger import logger as log
import help_funcs

tel_number = config.TELE_TWO_USERNAME
password = config.TELE_TWO_PASSWORD
base_url = config.TELE_TWO_BASE_URL


class TeleTwoParser:
    """ 
    Класс для парсинга данных сайта tele2
    Для получения данных симкарт
    """
    def __init__(self, base_url, username, password):
        """
        При инициализации принимает:
        1 Базовый адрес
        2 Логин
        3 Пароль
        Инициализируется браузер Chrome по удаленному серверу
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.options = Options()
        # CrossBrowser подключение к удаленному серверу
        self.browser = webdriver.Remote(
            command_executor=f"http://{config.USER_IP}:4444/wd/hub",
            options=self.options
        )

    def close_browser(self):
        """
        Метод для закрытия браузера
        """
        time.sleep(random.randint(10, 20))
        self.browser.quit()

    def enter_to_lk_page(self):
        """
        Метод для входа в личный кабинет
        """
        try:
            self.browser.get(self.base_url)
            log.info(f"Получена Главная страница")
            time.sleep(random.randint(1, 10))
            # Нажатие кнопки входа по паролю
            password_button = self.browser.find_element(By.XPATH, "//*[@id='keycloakLoginModal']/div/div/div/div/div[2]/div/div/div/div/div/button[2]")
            log.info(f"Кнопка входа по паролю: {password_button} найдена")
            time.sleep(random.randint(1, 10))
            password_button.click()
            log.info(f"Кнопка входа по паролю нажата")
            time.sleep(random.randint(1, 10))
            # Ввод номера телефона
            phone_field = self.browser.find_element(By.XPATH, "//*[@id='042c52bb8ed236b5eb5b22ecea0e4753']")
            log.info(f"Поле ввода номера телефона: {phone_field} найдено")
            time.sleep(random.randint(1, 10))
            phone_field.send_keys(self.username)
            log.info(f"Поле ввода номера телефона заполнено")
            time.sleep(random.randint(1, 10))
            # Ввод пароля
            password_field = self.browser.find_element(By.XPATH, "//*[@id='textField_password']")
            log.info(f"Поле ввода пароля: {password_field} найдено")
            time.sleep(random.randint(1, 10))
            password_field.send_keys(self.password)
            log.info(f"Поле ввода пароля заполнено")
            time.sleep(random.randint(1, 10))
            # Нажатие кнопки входа
            login_button = self.browser.find_element(By.XPATH, "//*[@id='keycloakLoginModal']/div/div/div/div/div[2]/form/div[2]/button[1]")
            log.info(f"Кнопка входа: {login_button} найдена")
            time.sleep(random.randint(1, 10))
            login_button.click()
            log.info(f"Кнопка входа нажата")
            time.sleep(random.randint(10, 20))

        except Exception as ex:
            log.error(f"Ошибка входа в личный кабинет: {ex}")
            self.browser.quit()
            return None

    def get_lk_page_title(self):
        """
        Метод для получения заголовка страницы
        Возвращает заголовок страницы:
        При успешном входе в личный кабинет: Tele2 - оператор мобильной связи
        """
        try:
            time.sleep(random.randint(10, 20))
            page_title = self.browser.title
            log.info(f"Заголовок страницы: {page_title}")
            return page_title
        except Exception as ex:
            log.error(f"Заголовок страницы не получен: {ex}")
            return None

    def go_to_first_abon_page(self):
        """
        Метод для перехода на первую страницу абонентов
        """
        try:
            time.sleep(random.randint(10, 20))
            self.browser.get(f"{self.base_url}/subscribers")
            log.info(f"Перешли на первую страницу абонентов {self.browser.title}")
            time.sleep(random.randint(10, 20))
        except Exception as ex:
            log.error(f"Перейти на первую страницу абонентов не получилось: {ex}")
            return None

    def get_abon_page_title(self):
        """
        Метод для получения заголовка страницы
        Возвращает заголовок страницы:
        При успешном входе в личный кабинет: Tele2 - оператор мобильной связи
        """
        try:
            time.sleep(random.randint(10, 20))
            page_title = self.browser.title
            log.info(f"Заголовок страницы: {page_title}")
            return page_title
        except Exception as ex:
            log.error(f"Заголовок страницы не получен: {ex}")
            return None

    def get_info_paginatios_pages(self):
        """
        Метод для получения страниц пагинации
        Отдаёт словарь с информацией о страницах:
        {
            "pagingPrevLink", или "pagingNextLink", или "pagingLinkPageЧисло": {
                "text": "Числи", или "<<", или ">>"
                "class": "curent", или "disabled", или " "
            }
        }

        """
        # Поиск элемента с классом "paging-links"
        try:
            paging_links_element = self.browser.find_element(By.CSS_SELECTOR, "span.paging-links")

        except Exception as ex:
            log.error(f"Не удалось найти элемент с пагинацией: {ex}")
            return None
        else:
            # Получение всех элементов пагинации
            pagination_elements = paging_links_element.find_elements(By.TAG_NAME, "a")
            pages = {}

            # Вывод информации о каждом элементе пагинации
            for pagination_element in pagination_elements:
                element_id = pagination_element.get_attribute("id")
                element_text = pagination_element.text
                element_class = pagination_element.get_attribute("class")

                pages[element_id] = {
                    "text": element_text,
                    "class": element_class
                }
                
            return pages

    def go_next_page(self):
        """
        Метод для перехода на следующую страницу
        """
        try:
            time.sleep(random.randint(10, 20))
            next_page = self.browser.find_element(By.XPATH, "//*[@id='pagingNextLink']")
            next_page.click()
            log.info(f"Перешли на следующую страницу")
            time.sleep(random.randint(10, 20))
        except Exception as ex:
            log.error(f"Перейти на следующую страницу не получилось: {ex}")
            return None

# Дальнейшие действия после


tele_two_parser = TeleTwoParser(base_url, tel_number, password)
# Вход в ЛК
tele_two_parser.enter_to_lk_page()
# Проверка корректности отдачи страницы
page_title = tele_two_parser.get_lk_page_title()
if page_title and 'мобильной связи' in str(page_title):
    print(f"Успешно залогинились в Лк: {page_title}")
    # Переход на первую страницу абонентов
    tele_two_parser.go_to_first_abon_page()
    # Проверка корректности отдачи страницы
    first_page_title = tele_two_parser.get_abon_page_title()
    if first_page_title and 'оператор мобильной' in str(first_page_title):
        print(f"Успешно перешли на первую страницу абонентов: {first_page_title}")
        # Получение сраниц для обхода
        pages = tele_two_parser.get_info_paginatios_pages()
        if pages != None:
            print(f"Текущая страница: {help_funcs.get_current_page(pages)} из {help_funcs.get_max_page(pages)}")
        else:
            print("Не удалось получить количество страниц для пагинации")
            print(f"Перезахожу на первую страницу абонентов")
            tele_two_parser.go_to_first_abon_page()
            second_try_page_title = tele_two_parser.get_abon_page_title()
            print(f"Успешно перешли на первую страницу абонентов: {second_try_page_title}")
            pages_second_try = tele_two_parser.get_info_paginatios_pages()
            if pages_second_try != None:
                print(f"Текущая страница: {help_funcs.get_current_page(pages_second_try)} из {help_funcs.get_max_page(pages_second_try)}")
            else:
                print("Не удалось получить количество страниц для пагинации")
                tele_two_parser.close_browser()


        # Переход на следующую страницу
        tele_two_parser.go_next_page()
        # Проверка корректности отдачи страницы
        next_page_title = tele_two_parser.get_abon_page_title()
        if next_page_title and 'оператор мобильной' in str(next_page_title):
            print(f"Успешно перешли на следующую страницу абонентов: {next_page_title}")
            pages = tele_two_parser.get_info_paginatios_pages()
            if pages != None:
                print(f"Текущая страница: {help_funcs.get_current_page(pages)} из {help_funcs.get_max_page(pages)}")
            else:
                print("Не удалось получить количество страниц для пагинации")
                tele_two_parser.close_browser()
        else:
            print("Не удалось перейти на следующую страницу")
            tele_two_parser.close_browser()


        
else:
    print("Не вошли")

tele_two_parser.close_browser()

