from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import random
from logger import logger as log


class TeleTwoParser:
    """ 
    Класс для парсинга данных сайта tele2
    Для получения данных симкарт
    """
    def __init__(self, base_url, username, password, user_ip):
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
            command_executor=f"http://{user_ip}:4444/wd/hub",
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
            time.sleep(random.randint(10, 20))
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
            time.sleep(random.randint(10, 40))

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

    def get_phones_from_page(self):
        """
        Метод для получения номеров абонентов
        Отдаёт список с номерами абонентов
        """
        try:
            time.sleep(random.randint(10, 20))
            msisdn_elements = self.browser.find_elements(By.CSS_SELECTOR, "div.subscriber-list__msisdn")

            phones = []

            for msisdn_element in msisdn_elements:
                
                phones.append(str(msisdn_element.text).replace(" ", "").replace("+", "").replace("-",""))
            return phones
        except Exception as ex:
            log.error(f"Получить номера абонентов не получилось: {ex}")
            return None




