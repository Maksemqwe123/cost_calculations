from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("<h1>Main Page</h1>")


def sign_in_user(request):
    return HttpResponse("<h1>Hello World</h1>")
