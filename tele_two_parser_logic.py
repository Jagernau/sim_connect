from tele_two_connect_selenium_remote import TeleTwoParser
import config
import help_funcs

tel_number = config.TELE_TWO_USERNAME
password = config.TELE_TWO_PASSWORD
base_url = config.TELE_TWO_BASE_URL
user_ip = config.USER_IP


tele_two_parser = TeleTwoParser(base_url, tel_number, password, user_ip)
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
        phones = tele_two_parser.get_phones_from_page()

        if phones != None:
            print(phones)
        else:
            print("Не удалось получить номера абонентов")
        # Получение сраниц для обхода
        pages = tele_two_parser.get_info_paginatios_pages()
        if pages != None:
            current_page = help_funcs.get_current_page(pages)
            max_page = help_funcs.get_max_page(pages)
            print(f"Текущая страница: {current_page} из {max_page}")
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
            phones_two = tele_two_parser.get_phones_from_page()
            print(phones_two)
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
    print("Не вошли по первой странице")
    tele_two_parser_second = TeleTwoParser("https://nnov.tele2.ru", tel_number, password, user_ip)
    tele_two_parser_second.enter_to_lk_page()
    print(tele_two_parser_second.get_lk_page_title())
    tele_two_parser_second.go_to_first_abon_page()
    print(tele_two_parser_second.get_abon_page_title())
    print(tele_two_parser_second.get_phones_from_page())
    pages = tele_two_parser_second.get_info_paginatios_pages()
    tele_two_parser_second.close_browser()

tele_two_parser.close_browser()
