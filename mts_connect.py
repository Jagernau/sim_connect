import requests
import json
from logger import logger as log
import config

# # Настройки
base_url = config.MTS_BASE_URL
username = config.MTS_USERNAME
password = config.MTS_PASSWORD
parent_tel_number = config.MTS_PARENT_TEL_NUMBER
account = config.MTS_ACCOUNT_NUMBER # Номер лицевого счёта

class MtsApi:
    def __init__(self, base_url, username, password, accountNo):
        """ 
        При инициализации принимает:
        1 Базовый адрес
        2 Логин в АПИ ЛК
        3 Пароль в АПИ ЛК
        4 Номер лицевого счёта
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.accountNo = accountNo
        self.access_token = None

    def get_access_token(self):
        url = f"{self.base_url}/token"
        auth = (f"{self.username}", f"{self.password}")
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(url, auth=auth, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            log.info(f"Получен токен доступа от МТС: {self.access_token}")
        else:
            log.error(f"Ошибка получения токена от МТС: {response.status_code} - {response.text}")

    def get_all_sims(self, parent_tel_number: str):
        """ 
        Метод для получения всех SIM-карт Не работает
        :param parent_tel_number: str
        :return: str
        """
        url = f"{self.base_url}/b2b/v1/Resources/GetAvailableSIM"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        data = {
        "Msisdn": f"{parent_tel_number}"
        }
        response = requests.post(url=url, headers=headers, data=data)
        return response.text

    def get_structure_abonents(self, pageNum: int): # Получение симок
        """ 
        Метод для получения структуры абонентов
        Принимает:
        1 Номер лицевого счёта self
        2 Номер страницы
        По умолчанию поставил количество результатов на странице: 10 
        :return: dict

        """
        url = f"{self.base_url}/b2b/v1/Service/HierarchyStructure?account={int(self.accountNo)}&pageNum={int(pageNum)}&pageSize=10"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(url=url, headers=headers)
        return response.json()

    def get_detail_internet_from_tel_number(self, tel_number): # Полный хаос не понятно
        """ 
        Метод предназначен для получения информации об остатках пакетов минут, интернет, SMS.
        Принимает:
        1 Номер телефона
        """
        url = f"{self.base_url}/b2b/v1/Bills/ValidityInfo?fields=MOAF&customerAccount.accountNo={tel_number}&customerAccount.productRelationship.product.productLine.name=Counters"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(url=url, headers=headers)
        return response.json()


    def get_detail_service_from_tel_number(self, tel_number):
        """ 
        Запрос списка подключенных услуг с указанием стоимости
        Принимает:
        1 Номер телефона
        """
        url = f"{self.base_url}/b2b/v1/Product/ProductInfo?category.name=MobileConnectivity&marketSegment.characteristic.name=MSISDN&marketSegment.characteristic.value={tel_number}&productOffering.actionAllowed=none&productOffering.productSpecification.productSpecificationType.name=service&fields=CalculatePrices&applyTimeZone"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(url=url, headers=headers)
        return response.json()

    def get_detail_location_from_tel_number(self, tel_number):
        """ 
        Определение страны пребывания абонента
        Принимает:
        1 Номер телефона
        """
        url = f"{self.base_url}/b2b/v1/Service/CurrentSubscriberLocation?msisdn={tel_number}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(url=url, headers=headers)
        return response.json()



mts_api = MtsApi(base_url, username, password, accountNo=account)
mts_api.get_access_token()
#all_sims = mts_api.get_all_sims(parent_tel_number)
#structure_abonents = mts_api.get_structure_abonents(pageNum=5)
#detail_internet = mts_api.get_detail_internet_from_tel_number()
#detail_service = mts_api.get_detail_service_from_tel_number()
#detail_location = mts_api.get_detail_location_from_tel_number()

# print(detail_location)
#
# with open('detail_location.json', 'w', encoding='utf-8') as file:
#     json.dump(detail_location, file, indent=2, ensure_ascii=False)
#

