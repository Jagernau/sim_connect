from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config
import time
from selenium.webdriver.common.by import By
import random

tel_number = config.TELE_TWO_USERNAME
password = config.TELE_TWO_PASSWORD

options = Options()

browser = webdriver.Remote(
    command_executor=f"http://{config.USER_IP}:4444/wd/hub",
    options=options
)

try:
    browser.get("https://newlk.tele2.ru")
    print(f"Сайт доступен: {browser.title}")

except Exception as ex:
    print(f"Сайт не доступен: {ex}")

time.sleep(random.randint(1, 10))

# Нажатие кнопки входа по паролю
try:
    password_button = browser.find_element(By.XPATH, "//*[@id='keycloakLoginModal']/div/div/div/div/div[2]/div/div/div/div/div/button[2]")
    print(f"Кнопка входа по паролю: {password_button} найдена")
except Exception as ex:
    print(f"Кнопка входа по паролю не найдена: {ex}")
    browser.quit()
else:
    try:
        password_button.click()
        print("Кнопка входа по паролю нажата")
    except Exception as ex:
        print(f"Кнопка входа по паролю не нажата : {ex}")
        browser.quit()

    else:
        time.sleep(random.randint(1, 10))
        # Ввод номера телефона
        try:
            phone_field = browser.find_element(By.XPATH, "//*[@id='042c52bb8ed236b5eb5b22ecea0e4753']")
            print(f"Поле ввода номера телефона: {phone_field} найдено")
        except Exception as ex:
            print(f"Поле ввода номера телефона не найдено: {ex}")
            browser.quit()
        else:
            try:
                phone_field.send_keys(str(tel_number))
                print("Поле ввода номера телефона заполнено")
            except Exception as ex:
                print(f"Поле ввода номера телефона не заполнено : {ex}")
                browser.quit()

            else:
                time.sleep(random.randint(1, 10))
        
                # Ввод пароля
                try:
                    password_field = browser.find_element(By.XPATH, "//*[@id='textField_password']")
                    print(f"Поле ввода пароля: {password_field} найдено")
                except Exception as ex:
                    print(f"Поле ввода пароля не найдено: {ex}")
                    browser.quit()
                else:
                    try:
                        password_field.send_keys(str(password))
                        print("Поле ввода пароля заполнено")
                    except Exception as ex:
                        print(f"Поле ввода пароля не заполнено : {ex}")
                        browser.quit()

                    else:
                        time.sleep(random.randint(1, 10))
                        try:
                        # Нажатие кнопки входа
                            login_button = browser.find_element(By.XPATH, "//*[@id='keycloakLoginModal']/div/div/div/div/div[2]/form/div[2]/button[1]")
                            print(f"Кнопка входа: {login_button} найдена")
                        except Exception as ex:
                            print(f"Кнопка входа не найдена: {ex}")
                            browser.quit()
                        else:                       
                            login_button.click()
                            print("Кнопка входа нажата")
                            time.sleep(random.randint(1, 10))


                            # Получение и вывод заголовка страницы
                            try:
                                page_title = browser.title
                                print(f"Заголовок страницы: {page_title}")
                            except Exception as ex:
                                print(f"Заголовок страницы не получен: {ex}")
                                browser.quit()
                            else:
                                print("Заголовок страницы получен")
                                time.sleep(random.randint(1, 10))

                                # Закрытие браузера
                                browser.quit()
