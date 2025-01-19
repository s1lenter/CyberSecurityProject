import pandas as pd
from multiprocessing import Pool


def get_year(date):
    if not pd.isna(date):
        return date[:4]
    return date


def chunk_analysis(chunk):
    chunk['published_at'] = chunk['published_at'].apply(get_year)
    chunk = chunk.dropna(subset=['key_skills']).reset_index()
    chunk = chunk.groupby('published_at')['key_skills'].apply('\r\n'.join).reset_index()
    return chunk


def process_chunks(chunks):
    with Pool() as pool:
        results = pool.map(chunk_analysis, chunks)
    res_dict = pd.concat(results, ignore_index=True).groupby('published_at')['key_skills']\
        .apply('\r\n'.join).reset_index()
    skills_list = res_dict['key_skills'].tolist()
    skills_str = '\r\n'.join(skills_list)
    skills = skills_str.replace('\r\n', '\n')
    skills_split_list = skills.split('\n')
    skills_count = {}
    for skill in skills_split_list:
        if skill in skills_count:
            skills_count[skill] += 1
        else:
            skills_count[skill] = 1
    return skills_count


def get_analysis(file_name, exit_csv, exit_html):
    chunks = pd.read_csv(file_name, chunksize=100000)
    results = process_chunks(chunks)
    df_results = pd.DataFrame(list(results.items()), columns=['Навык', 'Количество'])\
        .sort_values(by='Количество', ascending=False)[:20]
    df_results.to_csv(exit_csv, index=False)
    df_results.to_html(exit_html, index=False)


if __name__ == "__main__":
    get_analysis('vacancies_2024.csv', 'top-20.csv', 'top-20.html')