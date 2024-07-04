import requests
import json
from logger import logger as log
import config

# # Настройки
base_url = config.TELE_TWO_BASE_URL
login = config.TELE_TWO_USERNAME
password = config.TELE_TWO_PASSWORD
#
# # Формирование запроса на получение токена
url = f"{base_url}/openapi/v1/tokens-stub-m2m/get?login={login}&password={password}"
# # Отправка запроса
response = requests.get(url)
#
# # Обработка ответа

token_data = response.text
print(token_data)

