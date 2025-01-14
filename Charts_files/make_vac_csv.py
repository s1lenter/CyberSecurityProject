import pandas as pd
from multiprocessing import Pool

currency = pd.read_csv('currency.csv')
chunks = pd.read_csv('mini_vacs.csv', chunksize=100000)

def chunk_analysis(chunk):
    names = ['безопасность', 'защита', 'information security specialist', 'information security', 'фахівець служби безпеки', 'cyber security']
    df = chunk[chunk['name'].str.lower().apply(lambda x: any(sub.lower() in x for sub in names))]
    return df


def process_chunks(chunks):
    with Pool() as pool:
        results = pool.map(chunk_analysis, chunks)

    df = pd.concat(results, ignore_index=True)

    return df


if __name__ == "__main__":
    chunks = pd.read_csv('vacancies_2024.csv', chunksize=100000)
    result = process_chunks(chunks)
    result.to_csv('security_vacs.csv', index=False)