from django.shortcuts import render
from .models import *
from .api_handler import *

def main_page(request):
    return render(request, 'main_page.html')

def all_vacancies(request):
    info = AnalysisResult.objects.filter(isAll=True)
    return render(request, 'all_vacancies_info.html', {'info': info})

def prof_relevance(request):
    info = AnalysisResult.objects.filter(isAll=False)
    return render(request, 'all_vacancies_info.html', {'info': info[:2]})

def geography(request):
    info = AnalysisResult.objects.filter(isAll=False)
    return render(request, 'all_vacancies_info.html', {'info': info[2:4]})

def skills(request):
    info = AnalysisResult.objects.filter(isAll=False)
    return render(request, 'all_vacancies_info.html', {'info': info[4:]})

def vacancies_from_hh(request):
    info = get_vacancies()
    return render(request, 'hh_vacs.html', {'info': info})