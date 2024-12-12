from django.shortcuts import render
from .forms import UserRegister
from .models import *
from random import choice


def home(request):
    return render(request, 'home.html')


def registration(request):
    users = User.objects.all()
    users_list = [user.login for user in users]
    context = {
        'User': users
    }
    if request.method == 'POST':
        user_login = request.POST.get('login')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        if password != repeat_password:
            return render(request, 'registration.html', {'error': 'Пароли не совпадают'})
        elif user_login in users_list:
            return render(request, 'registration.html', {'error': 'Пользователь уже существует. Придумайте другой логин'})
        else:
            User.objects.create(login=user_login, password=password)
            return render(request, 'home.html')
    return render(request, 'registration.html', context)


def loging(request):
    users = User.objects.all()
    users_list = [user.login for user in users]
    passwords_list = [user.password for user in users]

    if request.method == 'POST':
        user_login = request.POST.get('login')
        password = request.POST.get('password')

        if user_login in users_list and password in passwords_list:
            if passwords_list.count(password) == 1:
                if users_list.index(user_login) == passwords_list.index(password):
                    return render(request, 'main.html')
                else:
                    return render(request, 'login.html', {'error': 'Неверный пароль'})
            elif passwords_list.count(password) > 1:
                cnt = 0
                for pas in range(len(passwords_list)):

                    if users_list.index(user_login) == passwords_list.index(password) + cnt:
                        return render(request, 'main.html')
                    cnt = 1

        else:
            return render(request,'login.html', {'error': 'Что-то пошло не так'})
    return render(request, 'login.html')


def helper(request):
    return render(request, 'helper.html')


def wait(request):
    return render(request, 'wait.html')


def main(request):
    if request.method == 'POST':
        something = request.POST.get('something')
        Randomaizer.objects.create(something=something)
        return render(request, 'main.html')
    return render(request, 'main.html')


def randoms(request):
        ran = Randomaizer.objects.all()
        ran_list = [i.something for i in ran]
        answer = choice(ran_list)
        slovo = ''.join(answer)
        return render(request, 'randoms.html', {'message': slovo})

