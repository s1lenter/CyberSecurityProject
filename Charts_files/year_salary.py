import pandas as pd
from multiprocessing import Pool

currency = pd.read_csv('currency.csv')
chunks = pd.read_csv('vacancies_2024.csv', chunksize=100000)


def change_currency(row):
    if pd.isna(row['salary']) or row['salary_currency'] == 'RUR':
        return row['salary']
    date = row['published_at'][:7]
    return row['salary'] * currency[currency['date'] == date][row['salary_currency']].tolist()[0]


def get_year(date):
    if not pd.isna(date):
        return date[:4]
    return date


def chunk_analysis(chunk):
    chunk['salary'] = chunk[['salary_from', 'salary_to']].mean(axis=1)
    df_cleaned = chunk.dropna(subset=['salary'])[['salary', 'published_at', 'salary_currency']]
    df_cleaned['salary'] = df_cleaned.apply(change_currency, axis=1)
    df_cleaned['published_at'] = df_cleaned['published_at'].apply(get_year)
    df_cleaned.drop(df_cleaned[df_cleaned['salary'] > 10000000].index, inplace=True)

    df = df_cleaned.groupby('published_at')['salary'].mean()
    return df.to_dict()


def process_chunks(chunks):
    with Pool() as pool:
        results = pool.map(chunk_analysis, chunks)

    final_result = {}
    for result in results:
        for year, salary in result.items():
            if year in final_result:
                final_result[year].append(salary)
            else:
                final_result[year] = [salary]

    for year in final_result:
        final_result[year] = sum(final_result[year]) / len(final_result[year])

    return final_result


if __name__ == "__main__":
    chunks = pd.read_csv('vacancies_2024.csv', chunksize=100000)
    results = process_chunks(chunks)
    df_results = pd.DataFrame(list(results.items()), columns=['Год', 'Средняя зарплата'])
    df_results['salary'] = df_results['salary'].round()
    df_results.to_csv('year_salary.csv', index=False)
    df_results.to_html('year_salary.html')