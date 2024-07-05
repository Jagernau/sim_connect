# Программа для сбора данных по сим от сотовых операторов
## Установка
1. Скопировать этот репозиторий в любой место: `git clone https://github.com/Jagernau/sim_connect`
2. Перейти в директорию `sim_connect`
3. Создать виртуальное окружение: `python3.10 -m venv venv`
4. Активировать виртуальное окружение: `source venv/bin/activate`
5. Установить зависимости: `pip install -r requirements.txt`
6. Создать файл .env: `touch .env` с конфигурацией:
    * Записать в фай .env следующие переменные:
    ```
    BILINE_BASE_URL=адрес сайта
    BILINE_CLIENT_ID=из АПИ
    BILINE_CLIENT_SECRET=из АПИ
    BILINE_USERNAME=логин
    BILINE_PASSWORD=пароль
    BILINE_DASHBORD=из АПИ

    MTS_BASE_URL=адрес сайта
    MTS_USERNAME=из АПИ
    MTS_PASSWORD=из АПИ
    MTS_PARENT_TEL_NUMBER=корпоративный номер
    MTS_ACCOUNT_NUMBER=лицевой счёт

    TELE_TWO_BASE_URL=адрес сайта
    TELE_TWO_USERNAME=логин
    TELE_TWO_PASSWORD=пароль

    USER_IP=ip адрес компьютера
    ```
7. Запустить драйвера браузеров для парсера Selenium под Теле2:
    * Перейти в директорию `selenium_docker_drivers/`
    * Запустить `sudo docker-compose up -d `

## Использование
На данном этапе логика по сбору данных разрабатывается и тестово программой получаются данные с Bilain Api, Mts Api. Написано корректное подключение к контейнерным браузерам для парсинга Теле2, через личный кабинет с помощью Selenium, так как у Теле2 отсутствует Api.
Представлены отдельные файлы для сбора данных по сим от сотовых операторов.
Версия Selenium актуальна на текущий месяц.

