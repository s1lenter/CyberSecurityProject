import year_count, year_salary, city_salary, city_part, top

if __name__ == "__main__":
    year_salary.get_analysis('security_vacs.csv', 'sec_year_salary.csv', 'sec_year_salary.html')
    year_count.get_analysis('security_vacs.csv', 'sec_year_count.csv', 'sec_year_count.html')
    city_salary.get_analysis('security_vacs.csv', 'sec_city_salary.csv', 'sec_city_salary.html')
    city_part.get_analysis('security_vacs.csv', 'sec_city_part.csv', 'sec_city_part.html')
    top.get_analysis('security_vacs.csv', 'sec_top.csv', 'sec_top.html')