from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config
import time
from selenium.webdriver.common.by import By
import random
from logger import logger as log

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
        :return: str
        """
        try:
            time.sleep(random.randint(10, 20))
            page_title = self.browser.title
            log.info(f"Заголовок страницы: {page_title}")
            return page_title
        except Exception as ex:
            log.error(f"Заголовок страницы не получен: {ex}")
            self.browser.quit()
            return None


tele_two_parser = TeleTwoParser(base_url, tel_number, password)

tele_two_parser.enter_to_lk_page()
page_title = tele_two_parser.get_lk_page_title()
if page_title and 'мобильной связи' in str(page_title):
    print(f"Заголовок страницы: {page_title}")
else:
    print("Заголовок страницы не получен")
tele_two_parser.close_browser()

