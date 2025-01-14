from django.shortcuts import render
from .models import *
from .api_handler import *

def main_page(request):
    return render(request, 'main_page.html', {'page_selected': 0})

def all_vacancies(request):
    info = AnalysisResult.objects.filter(isAll=True)
    return render(request, 'all_vacancies_info.html', {'info': info, 'page_selected': 1})

def prof_relevance(request):
    info = AnalysisResult.objects.filter(isAll=False)
    return render(request, 'all_vacancies_info.html', {'info': info[:2], 'page_selected': 2})

def geography(request):
    info = AnalysisResult.objects.filter(isAll=False)
    return render(request, 'all_vacancies_info.html', {'info': info[2:4], 'page_selected': 3})

def skills(request):
    info = AnalysisResult.objects.filter(isAll=False)
    return render(request, 'all_vacancies_info.html', {'info': info[4:], 'page_selected': 4})

def vacancies_from_hh(request):
    info = get_vacancies()
    return render(request, 'hh_vacs.html', {'info': info, 'page_selected': 5})