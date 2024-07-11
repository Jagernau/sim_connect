import json


def collect_keys(data, keys=None):
    if keys is None:
        keys = set()
    
    if isinstance(data, dict):
        for key, value in data.items():
            keys.add(key)
            collect_keys(value, keys)
    elif isinstance(data, list):
        for item in data:
            collect_keys(item, keys)
    
    return keys

with open('all_sims_page_beeline_6.json', 'r') as file:
    json_data = json.load(file)

# Использование функции collect_keys
all_keys = collect_keys(json_data)
print(all_keys)
