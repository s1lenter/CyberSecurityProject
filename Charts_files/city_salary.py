import pandas as pd
from multiprocessing import Pool

currency = pd.read_csv('currency.csv')


def change_currency(row):
    if pd.isna(row['salary']) or row['salary_currency'] == 'RUR':
        return row['salary']
    date = row['published_at'][:7]
    return row['salary'] * currency[currency['date'] == date][row['salary_currency']].tolist()[0]


def chunk_analysis(chunk):
    chunk['salary'] = chunk[['salary_from', 'salary_to']].mean(axis=1)
    df_cleaned = chunk.dropna(subset=['salary'])[['salary', 'published_at', 'area_name', 'salary_currency']]
    df_cleaned['salary'] = df_cleaned.apply(change_currency, axis=1)
    df_cleaned.drop(df_cleaned[df_cleaned['salary'] > 10000000].index, inplace=True)

    df = df_cleaned.groupby(['area_name']).agg({
            "salary": "mean",
            "published_at": "count"
        }).reset_index()
    return df


def process_chunks(chunks):
    with Pool() as pool:
        results = pool.map(chunk_analysis, chunks)
    df = pd.concat(results, ignore_index=True)
    result_df = df.groupby(['area_name']).agg({
        "salary": "mean",
        "published_at": "sum"
    }).reset_index()
    return result_df


def get_analysis(file_name, exit_csv, exit_html):
    chunks = pd.read_csv(file_name, chunksize=100000)
    df_results = process_chunks(chunks)
    df_results.columns = ['Город', 'Средняя зарплата', 'count']
    df_results['count'] = round(df_results['count'] / df_results['count'].sum(), 3)
    df_results = df_results[df_results['count'] >= 0.01] \
        .sort_values(by='Средняя зарплата', ascending=False).reset_index(drop=True)
    df_results.index += 1
    df_results['Средняя зарплата'] = df_results['Средняя зарплата'].round()
    df_cleaned = df_results[['Город', 'Средняя зарплата']].dropna(subset='Средняя зарплата')
    df_cleaned.to_csv(exit_csv, index=False)
    df_cleaned.to_html(exit_html, index=False)


if __name__ == "__main__":
    get_analysis('vacancies_2024.csv', 'city_salary.csv', 'city_salary.html')