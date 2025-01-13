import pandas as pd
from multiprocessing import Pool

currency = pd.read_csv('currency.csv')
chunks = pd.read_csv('mini_vacs.csv', chunksize=100000)


def chunk_analysis(chunk):
    df = chunk.groupby('area_name')['name'].count()
    return df.to_dict()


def process_chunks(chunks):
    with Pool() as pool:
        results = pool.map(chunk_analysis, chunks)

    final_result = {}
    for result in results:
        for year, count in result.items():
            if year in final_result:
                final_result[year] += count
            else:
                final_result[year] = count

    return final_result
#
# for chunk in chunks:
#     x = chunk_analysis(chunk)
#     print()

if __name__ == "__main__":
    chunks = pd.read_csv('vacancies_2024.csv', chunksize=100000)
    results = process_chunks(chunks)
    df_results = pd.DataFrame(list(results.items()), columns=['Город', 'Доля вакансий'])
    all_vacs = df_results['Доля вакансий'].sum()
    df_results['Доля вакансий'] = round(df_results['Доля вакансий'] / all_vacs, 3)
    df_results = df_results[df_results['Доля вакансий'] >= 0.01]\
        .sort_values(by='Доля вакансий', ascending=False).reset_index(drop=True)
    df_results.to_csv('city_part.csv', index=False)
    df_results.to_html('city_part.html', index=False)