from datetime import datetime, timedelta

import xml.etree.ElementTree as ET
import requests


def change_currency(number, curr, currency_dict):
    if curr != 'RUR':
        return number * currency_dict[curr]
    return number


def get_currency():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    curr = {}
    for valute in root.findall('Valute'):
        char_code = valute.find('CharCode').text
        value = float(valute.find('Value').text.replace(',', '.'))
        curr[char_code] = value
    return curr


def get_vacancies():
    currency = get_currency()
    keys = ['id', 'name', 'employer', 'area', 'salary', 'published_at', 'description', 'skills']
    date_from = (datetime.now() - timedelta(hours=24)).isoformat() + 'Z'
    params = {
        'date_from': date_from,
        'text': f'name:(Специалист по информационной безопасности)',
        'per_page': 10,
        'page': 0
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    result = {}
    resp_json = response.json()['items']
    data = sorted(
        resp_json,
        key=lambda x: datetime.strptime(x['published_at'], "%Y-%m-%dT%H:%M:%S%z"),
        reverse=True
    )[:10]
    result_list = []
    for item in data:
        info_list = {}
        cur_vac = requests.get(f"https://api.hh.ru/vacancies/{item['id']}", params=params)
        data = cur_vac.json()
        item['description'] = data['description']
        item['skills'] = [d['name'] for d in data['key_skills']]
        for key in keys:
            if key == 'area' or key == 'employer':
                info_list[key] = item[key]['name']
            elif key == 'skills':
                if len(item[key]) > 0:
                    info_list[key] = ', '.join(item[key])
                else: info_list[key] = 'Необходимые навыки не указаны'
            elif key == 'published_at':
                info_list[key] = f"{item[key][8:10]}-{item[key][5:7]}-{item[key][:4]} {item[key][11:16]}"
            elif key == 'salary' and item[key] is None:
                info_list[key] = 'Зарплата не указана'
            elif key == 'salary' and item[key]['to'] is None:
                info_list[key] = f'От {item[key]["from"]} ({item[key]["currency"]})'
            elif key == 'salary' and item[key]['from'] is None:
                info_list[key] = f'До {item[key]["to"]} ({item[key]["currency"]})'
            elif key == 'salary' and item[key]:
                info_list[key] = f'От {item[key]["from"]} до {item[key]["to"]} ({item[key]["currency"]})'
            else:
                info_list[key] = item[key]
        result[item['id']] = info_list
        result_list = [value for value in result.values()]
    return result_list
get_vacancies()