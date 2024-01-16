from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

# Create your views here.


def index(request):
    return HttpResponse("<h1>Main Page</h1>")


@csrf_protect
def sign_in_user(request):
    context = {
        'css_path': 'css/styles.css'
    }
    login = request.POST['login']
    password = request.POST['password']
    print(login)
    print(password)
    return render(request, 'form_sign_in.html', context)
