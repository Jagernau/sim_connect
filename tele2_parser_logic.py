from tele_two_connect_selenium_remote import TeleTwoParser
import config
import help_funcs
import json

tel_number = config.TELE_TWO_USERNAME
password = config.TELE_TWO_PASSWORD
base_url = config.TELE_TWO_BASE_URL
user_ip = config.USER_IP


tele_two_parser = TeleTwoParser(base_url, tel_number, password, user_ip)
tele_two_parser.enter_to_lk_page()

if 'мобильной связи' in str(tele_two_parser.get_lk_page_title()):
    tele_two_parser.go_to_first_abon_page()
    if 'оператор мобильной' in str(tele_two_parser.get_abon_page_title()):
        
        all_phones = []

        all_pages = tele_two_parser.get_info_paginatios_pages()
        for i in range(help_funcs.get_max_page(all_pages)):
            pagination_info = tele_two_parser.get_info_paginatios_pages()
            current_page = help_funcs.get_current_page(pagination_info)
            if current_page == 3:
                # остановить цикл
                break
            else:
                all_phones.append({'page':current_page, 'phones':tele_two_parser.get_phones_from_page()})
                tele_two_parser.go_next_page()


        all_info = []
        for i in all_phones:
            page = i['page']
            phones = i['phones']
            for phone in phones:
                # если телефон не пустой ''
                if phone != '':
                   detail_info = tele_two_parser.go_detail_page_get_info(phone)
                   all_info.append({'page':page, 'phone':phone, 'detail_info':detail_info})

        # save to json
        with open('data_tele2.json', 'w', encoding='utf-8') as file:
            json.dump(all_info, file, ensure_ascii=False, indent=4)
                                            
    else:
        print("Не удалось перейти на первую страницу абонентов")
        tele_two_parser.close_browser()
else:
    print("Не удалось залогинится в ЛК")
    tele_two_parser.close_browser()




