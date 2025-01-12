import pandas as pd
from multiprocessing import Pool

currency = pd.read_csv('currency.csv')
chunks = pd.read_csv('mini_vacs.csv', chunksize=100000)



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

    df = df_cleaned.groupby('area_name')['salary'].mean()
    return df.to_dict()


def process_chunks(chunks):
    with Pool() as pool:
        results = pool.map(chunk_analysis, chunks)

    final_result = {}
    for result in results:
        for city, salary in result.items():
            if city in final_result:
                final_result[city].append(salary)
            else:
                final_result[city] = [salary]

    for year in final_result:
        final_result[year] = sum(final_result[year]) / len(final_result[year])

    return final_result

# for chunk in chunks:
#     x = chunk_analysis(chunk)
#     print(x)


if __name__ == "__main__":
    chunks = pd.read_csv('vacancies_2024.csv', chunksize=100000)
    results = process_chunks(chunks)
    df_results = pd.DataFrame(list(results.items()), columns=['Город', 'Зп']).sort_values(by='Зп', ascending=False)
    df_results.to_csv('city_salary.csv', index=False)