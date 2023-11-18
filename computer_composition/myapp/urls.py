from django.urls import path
from .views import *

urlpatterns = [
    path('upload_excel', upload_excel, name='upload_excel'),
    path('clear_database', clear_database, name='clear_database'),
    path('get_information', get_information, name='get_information')
]
