import numpy as np
import pandas as pd
import requests

url = 'http://www.cbr.ru/scripts/XML_daily.asp'

columns = ['date','BYR','USD','EUR','KZT','UAH','AZN','KGS','UZS','GEL']
first_days = pd.date_range(start='2003-01-01', end='2024-11-30', freq='MS')
first_days_list = first_days.tolist()
dates = [x.strftime('%d/%m/%Y') for x in first_days_list]
df = pd.DataFrame(columns=columns)


def get_curr(code):
    value = curr_date_df[curr_date_df['CharCode'] == code]['Value'].tolist()
    nominal = curr_date_df[curr_date_df['CharCode'] == code]['Nominal'].tolist()
    if len(value) != 0:
        value = float(value[0].replace(',', '.')) / nominal[0]
        if code == 'BYR':
            return round(value, 8)
        elif code == 'KZT':
            return round(value, 6)
        elif code == 'UAH':
            return round(value, 5)
        elif code == 'KGS':
            return round(value, 6)
        elif code == 'UZS':
            return round(value, 8)
        return value
    return np.nan


for date in dates:
    new_date = f"{date[-4:]}-{date[-7:-5]}"
    response = requests.get(url+'?date_req='+date)
    content = response.content.decode("windows-1251")
    curr_date_df = pd.read_xml(content)
    curr_list = []
    for col in columns:
        if col == 'date':
            curr_list.append(new_date)
        else:
            curr_list.append(get_curr(col))
    df = pd.concat([df,pd.DataFrame([curr_list], columns=columns)], ignore_index=True)

df.to_csv('currency.csv', index=False)