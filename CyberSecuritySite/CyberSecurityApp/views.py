from django.shortcuts import render
from .models import *


def main_page(request):
    return render(request, 'main_page.html')

def all_vacancies(request):
    info = AnalysisResult.objects.filter(isAll=True)
    return render(request, 'all_vacancies_info.html', {'info' : info})
