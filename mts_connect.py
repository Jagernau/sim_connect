import requests
import json
from logger import logger as log
import config

# # Настройки
base_url = config.MTS_BASE_URL
username = config.MTS_USERNAME
password = config.MTS_PASSWORD
parent_tel_number = config.MTS_PARENT_TEL_NUMBER

class MtsApi:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
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
        url = f"{self.base_url}/b2b/v1/Resources/GetAvailableSIM"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        data = {
        "Msisdn": f"{parent_tel_number}",
        }
        response = requests.post(url=url, headers=headers, data=data)
        return response.text


biline_api = MtsApi(base_url, username, password)
biline_api.get_access_token()
all_sims = biline_api.get_all_sims(parent_tel_number)
print(all_sims)

