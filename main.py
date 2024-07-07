import re
import requests
import json

BASE_URL = 'https://asu.pnu.edu.ua/2023-2024-2/static/groups/1002/008020/'
MINOR_URL = BASE_URL + 'index.js?v=202406041044'

try:
    response = requests.get(MINOR_URL)
    response.raise_for_status()

    if response.content:
        response_text = response.text
        json_text = response_text.split('const PNUschedule=')[1]
        json_text = json_text.rsplit('];', 1)[0] + ']'
        json_text = re.sub(r'(\[|\])', '', json_text)
        json_text = re.sub(r'([{,]\s*)(\w+)(\s*):', r'\1"\2":', json_text)
        json_objects = json_text.split('},')
        json_objects = [obj + '}' for obj in json_objects]
        
        unique_subjects = set()
        special_subjects = []
        
        for obj in json_objects:
            try:
                data = json.loads(obj)
                subject = data.get('l')
                if subject:
                    if "Письм.Екз." in subject:
                        special_subjects.append(subject)
                    else:
                        unique_subjects.add(subject)
            except json.JSONDecodeError as json_err:
                print(f"JSON decode error: {json_err}")
                
        print("Назви предметів у таблицю без повторень:")
        for subject in unique_subjects:
            print(subject)
            
        print("\nПредмети з 'Письм.Екз.' у кінець списку:")
        for subject in special_subjects:
            print(subject)
    else:
        print("Відповідь від сервера порожня")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as req_err:
    print(f"Error occurred: {req_err}")
except ValueError as json_err:
    print(f"JSON decode error: {json_err}")