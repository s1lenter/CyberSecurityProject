import pandas as pd
from multiprocessing import Pool

currency = pd.read_csv('currency.csv')
chunks = pd.read_csv('mini_vacs.csv', chunksize=100000)


def get_year(date):
    if not pd.isna(date):
        return date[:4]
    return date


def chunk_analysis(chunk):
    chunk['published_at'] = chunk['published_at'].apply(get_year)

    df = chunk.groupby('published_at')['name'].count()
    return df.to_dict()


def process_chunks(chunks):
    with Pool() as pool:
        results = pool.map(chunk_analysis, chunks)

    # Объединяем все словари в один
    final_result = {}
    for result in results:
        for year, count in result.items():
            if year in final_result:
                final_result[year] += count
            else:
                final_result[year] = count

    return final_result


if __name__ == "__main__":
    chunks = pd.read_csv('vacancies_2024.csv', chunksize=100000)
    results = process_chunks(chunks)
    df_results = pd.DataFrame(list(results.items()), columns=['Год', 'Количество вакансий'])
    df_results.to_csv('year_count.csv', index=False)