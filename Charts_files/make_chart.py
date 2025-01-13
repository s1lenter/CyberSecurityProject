import pandas as pd
import matplotlib.pyplot as plt


def make_column_chart(file, title, x_name, y_name):
    df = pd.read_csv(file)

    df[x_name] = pd.to_numeric(df[x_name])

    plt.figure(figsize=(10, 6))
    plt.bar(df[x_name], df[y_name])
    plt.title(title)
    plt.xticks(df[x_name], rotation=90)
    plt.grid(axis='y')
    plt.show()

def horizontal_chart(file, title, x_name, y_name):
    df = pd.read_csv(file).sort_values(by='Средняя зарплата')
    plt.figure(figsize=(14, 10))
    plt.barh(df[x_name], df[y_name])
    plt.title(title)
    plt.grid(axis='x')
    plt.show()

def make_pie(file, title, x_name, y_name):
    df = pd.read_csv(file)
    value = round(1 - df[x_name].sum(), 3)
    more = pd.DataFrame({y_name: ['Другие города'], x_name: [value]})
    df = pd.concat([df, more], ignore_index=True)
    plt.figure(figsize=(10, 10))
    plt.pie(df[x_name], labels=df[y_name], labeldistance=1.1)
    plt.axis('equal')
    plt.title(title)
    plt.show()


# make_column_chart('year_salary.csv', 'Динамика уровня зарплат по годам', 'Год', 'Средняя зарплата')
# make_column_chart('year_count.csv', 'Динамика количества вакансий по годам', 'Год', 'Количество вакансий')
# horizontal_chart('city_salary.csv', 'Уровень зарплат по городам', 'Город', 'Средняя зарплата')
make_pie('city_part.csv', 'Доля вакансий по городам', 'Доля вакансий', 'Город')
