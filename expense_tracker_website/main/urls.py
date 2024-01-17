from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('sign-in', views.sign_in_user),
    path('expenditure_results', views.view_all_records, name='expenditure_results')  # Переписать функцию view_all_records
]
