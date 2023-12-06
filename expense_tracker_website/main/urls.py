from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('sign-in', views.sign_in_user)
]
