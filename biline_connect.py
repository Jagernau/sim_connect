import requests
import json
from logger import logger as log
import config


# # Настройки
base_url = config.BILINE_BASE_URL
client_id = config.BILINE_CLIENT_ID
client_secret = config.BILINE_CLIENT_SECRET
username = config.BILINE_USERNAME
password = config.BILINE_PASSWORD
dashboard_id = config.BILINE_DASHBORD

class BilineApi:
    def __init__(self, base_url, client_id, client_secret, username, password):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = None

    def get_access_token(self):
        """
        Метод для получения токена доступа
        :return: str
        """
        url = f"{self.base_url}/oauth/token"
        data = {
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "password"
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            log.info(f"Получен токен доступа от Билайн: {self.access_token}")
        else:
            log.error(f"Ошибка получения токена от Билайн: {response.status_code} - {response.text}")


    def get_all_sims_pag(self, dashboard_id: str, page: str):
        """ 
        Метод для получения всех SIM-карт Требуется пагинация
        :param dashboard_id: str
        :param page: int
        :return: dict
        """
        url = f"{self.base_url}/api/v0/dashboards/{dashboard_id}/sim_cards/list_all_sim"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "X-Requested-With": "XMLHttpRequest"
        }
        payload = {
                "page": int(page)
        }


        response = requests.post(url=url, headers=headers, data=payload)

        return response.json()

    def get_all_services(self, dashboard_id: str):
        """ 
        Выводит все услуги 
        :param dashboard_id: str
        :return: {}
        """
        url = f"{self.base_url}/api/v0/dashboards/{dashboard_id}/communication_plans"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "X-Requested-With": "XMLHttpRequest"
        }
        response = requests.post(url=url, headers=headers)
        return response.json()
    def get_detail_services_name(self, dashboard_id: str, tarif_name: str):
        """ 
        Выводит услугу по имени 
        :param dashboard_id: str
        :return: {}
        """
        url = f"{self.base_url}/api/v0/dashboards/{dashboard_id}/communication_plans"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "X-Requested-With": "XMLHttpRequest"
        }
        payload = {
                "query": {
                    "name": {
                        "value": f'{tarif_name}',
                        "type": "search"
                        }
                }
        }
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        return response.json()

    def get_sims_paginations(self, dashboard_id: str, tarif_name: str):
        """ 
        Отдаёт сим по пагинации
        :param dashboard_id: str
        :return: {}
        """
        url = f"{self.base_url}/api/v0/dashboards/{dashboard_id}/communication_plans"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "X-Requested-With": "XMLHttpRequest"
        }
        payload = {
                "query": {
                    "name": {
                        "value": f'{tarif_name}',
                        "type": "search"
                        }
                }
        }
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        return response.json()

biline_api = BilineApi(base_url, client_id, client_secret, username, password)
biline_api.get_access_token()
all_sims = biline_api.get_all_sims_pag(dashboard_id, page=5)
#all_serv = biline_api.get_all_services(dashboard_id)
#detail_serv_name = biline_api.get_detail_services_name(dashboard_id, "Beeline Russia CSD 20 GRPS LTE")


with open('all_sims_page_beeline_5.json', 'w', encoding='utf-8') as file:
    json.dump(all_sims, file, indent=2, ensure_ascii=False)

