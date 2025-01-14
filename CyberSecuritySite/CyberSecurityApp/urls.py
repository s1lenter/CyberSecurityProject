from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('all_vacancies/', all_vacancies, name='all_vacancies'),
    path('prof_relevance', prof_relevance, name='prof_relevance'),
    path('geography', geography, name='geography'),
    path('skills', skills, name='skills'),
    path('vacs_from_hh', vacancies_from_hh, name='vacs_from_hh')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)