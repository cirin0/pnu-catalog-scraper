import requests
import json
import re

BASE_URL = 'https://asu.pnu.edu.ua/2023-2024-2/static/groups/1002/009705/'
MINOR_URL = BASE_URL + 'index.js?v=202406041044'


def extract_json(response_text):
    """Extracts and cleans the JSON data from the response text."""
    json_text = response_text.split('const PNUschedule=')[
        1].rsplit('];', 1)[0] + ']'
    json_text = json_text.replace('[', '').replace(']', '')
    json_text = re.sub(r'([{,]\s*)(\w+)(\s*):', r'\1"\2":', json_text)
    return json_text


def parse_subjects(json_text):
    """Parses subject names from JSON, separating special subjects."""
    unique_subjects = set()
    special_subjects = []

    for obj_str in json_text.split('},'):
        try:
            data = json.loads(obj_str + '}')
            subject = data.get('l')
            if subject:
                if "Письм.Екз." in subject:
                    special_subjects.append(subject)
                else:
                    unique_subjects.add(subject)
        except json.JSONDecodeError:
            pass  # Handle potential errors gracefully

    return unique_subjects, special_subjects


def save_to_csv(unique_subjects, special_subjects):
    """Saves the subject names to a TXT file."""
    with open('subjects.txt', 'w', encoding='utf-8') as file:
        file.write('Назви предметів\n')
        for subject in unique_subjects:
            file.write(subject + '\n')

        file.write('\nНазви предметів (екзамен)\n')
        for subject in special_subjects:
            file.write(subject + '\n')


def main():
    try:
        response = requests.get(MINOR_URL)
        response.raise_for_status()

        if response.content:
            json_text = extract_json(response.text)
            unique_subjects, special_subjects = parse_subjects(json_text)

            print("Назви предметів у таблицю без повторень:")
            for subject in unique_subjects:
                print(subject)

            print("\nПредмети з 'Письм.Екз.' у кінець списку:")
            for subject in special_subjects:
                print(subject)

            save_to_csv(unique_subjects, special_subjects)
            print("Дані збережено у файл subjects.csv")

        else:
            print("Відповідь від сервера порожня")

    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")


if __name__ == "__main__":
    main()
