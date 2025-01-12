import pandas as pd
import matplotlib.pyplot as plt

def make_column_chart(file, title, x_name, y_name):
    df_results = pd.read_csv(file)

    df_results[x_name] = pd.to_numeric(df_results[x_name])

    plt.figure(figsize=(10, 6))
    plt.bar(df_results[x_name], df_results[y_name])
    plt.title(title)
    plt.xticks(df_results[x_name], rotation=90)
    plt.grid(axis='y')
    plt.show()

make_column_chart('year_count.csv', 'Количество вакансий по годам', 'Год', 'Количество вакансий')