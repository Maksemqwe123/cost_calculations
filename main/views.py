from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from cryptography.fernet import Fernet
import os

from .models import UserRegistration


def index(request):
    return HttpResponse("<h1>Main Page</h1>")


@csrf_protect
def sign_in_user(request):
    all_records = UserRegistration.objects.all()

    if request.method == 'POST':
        cipher_suite = Fernet(os.getenv('FERNET_KEY'))

        login_input = request.POST['login']
        password_input = request.POST['password']

        condition = True  # Здесь вы можете определить условие для проверки

        context = {
            'condition': condition,
            "error_message": "Неверный пароль"
        }

        for info in all_records:
            login = info.login
            password = info.password

            decrypted_login = cipher_suite.decrypt(login)
            decrypted_password = cipher_suite.decrypt(password)

            if decrypted_login.decode().lower() == login_input.lower() and decrypted_password.decode().lower() == password_input.lower():
                return redirect('expenditure_results')
            else:
                messages.error(request, 'Неправильный пароль')
                return render(request, 'form_sign_in.html', context=context)

    elif request.method == 'GET':
        condition = False

        context = {
            'condition': condition
        }

        return render(request, 'form_sign_in.html', context)


def view_all_records(request):  # Переписать функцию view_all_records
    return render(request, 'index.html')

